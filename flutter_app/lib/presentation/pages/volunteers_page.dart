import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../core/theme/app_theme.dart';
import '../../core/database/database_helper_new.dart';
import '../../data/models/volunteer.dart';

// Provider for volunteers list
final volunteersProvider = FutureProvider<List<Volunteer>>((ref) async {
  final maps = await DatabaseHelper.instance.getVolunteers();
  return List.generate(maps.length, (i) => Volunteer.fromMap(maps[i]));
});

// Provider for selected volunteer
final selectedVolunteerProvider = StateProvider<Volunteer?>((ref) => null);

// Provider for search query
final volunteerSearchProvider = StateProvider<String>((ref) => '');

// Provider for filtered volunteers
final filteredVolunteersProvider = Provider<AsyncValue<List<Volunteer>>>((ref) {
  final volunteersAsync = ref.watch(volunteersProvider);
  final searchQuery = ref.watch(volunteerSearchProvider);
  
  return volunteersAsync.when(
    data: (volunteers) {
      if (searchQuery.isEmpty) {
        return AsyncValue.data(volunteers);
      }
      final filtered = volunteers.where((volunteer) {
        return volunteer.name.toLowerCase().contains(searchQuery.toLowerCase()) ||
               (volunteer.email?.toLowerCase().contains(searchQuery.toLowerCase()) ?? false) ||
               (volunteer.phone?.contains(searchQuery) ?? false);
      }).toList();
      return AsyncValue.data(filtered);
    },
    loading: () => const AsyncValue.loading(),
    error: (error, stack) => AsyncValue.error(error, stack),
  );
});

class VolunteersPage extends ConsumerWidget {
  const VolunteersPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header
            _buildHeader(context, ref),
            const SizedBox(height: 24),
            
            // Main content
            Expanded(
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Left panel - Volunteer list
                  Expanded(
                    flex: 2,
                    child: _buildVolunteerList(context, ref),
                  ),
                  const SizedBox(width: 24),
                  
                  // Right panel - Volunteer details
                  Expanded(
                    flex: 1,
                    child: _buildVolunteerDetails(context, ref),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildHeader(BuildContext context, WidgetRef ref) {
    return Row(
      children: [
        // Title section
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                '👥 Volunteer Management',
                style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                  fontWeight: FontWeight.bold,
                  color: AppTheme.primaryGreen,
                ),
              ),
              const SizedBox(height: 4),
              Text(
                'Manage volunteer information and track participation',
                style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                  color: Theme.of(context).textTheme.bodyMedium?.color,
                ),
              ),
            ],
          ),
        ),
        
        // Search and actions
        SizedBox(
          width: 300,
          child: Row(
            children: [
              // Search field
              Expanded(
                child: TextField(
                  decoration: InputDecoration(
                    hintText: 'Search volunteers...',
                    prefixIcon: const Icon(Icons.search),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                    contentPadding: const EdgeInsets.symmetric(
                      horizontal: 16,
                      vertical: 12,
                    ),
                  ),
                  onChanged: (value) {
                    ref.read(volunteerSearchProvider.notifier).state = value;
                  },
                ),
              ),
              const SizedBox(width: 12),
              
              // Add volunteer button
              ElevatedButton.icon(
                onPressed: () => _showAddVolunteerDialog(context, ref),
                icon: const Icon(Icons.add),
                label: const Text('Add'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppTheme.primaryGreen,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(
                    horizontal: 16,
                    vertical: 12,
                  ),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildVolunteerList(BuildContext context, WidgetRef ref) {
    final volunteersAsync = ref.watch(filteredVolunteersProvider);
    final selectedVolunteer = ref.watch(selectedVolunteerProvider);

    return Card(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // List header
          Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                const Icon(Icons.people, color: AppTheme.primaryGreen),
                const SizedBox(width: 8),
                Text(
                  'Volunteers',
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const Spacer(),
                volunteersAsync.when(
                  data: (volunteers) => Chip(
                    label: Text('${volunteers.length}'),
                    backgroundColor: AppTheme.primaryGreen.withOpacity(0.1),
                  ),
                  loading: () => const SizedBox.shrink(),
                  error: (_, __) => const SizedBox.shrink(),
                ),
              ],
            ),
          ),
          const Divider(height: 1),
          
          // Volunteer list
          Expanded(
            child: volunteersAsync.when(
              data: (volunteers) {
                if (volunteers.isEmpty) {
                  return _buildEmptyState(context);
                }
                
                return ListView.builder(
                  itemCount: volunteers.length,
                  itemBuilder: (context, index) {
                    final volunteer = volunteers[index];
                    final isSelected = selectedVolunteer?.id == volunteer.id;
                    
                    return _buildVolunteerCard(
                      context,
                      ref,
                      volunteer,
                      isSelected,
                    );
                  },
                );
              },
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (error, _) => Center(
                child: Text('Error loading volunteers: $error'),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildVolunteerCard(
    BuildContext context,
    WidgetRef ref,
    Volunteer volunteer,
    bool isSelected,
  ) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      child: Material(
        borderRadius: BorderRadius.circular(8),
        color: isSelected 
          ? AppTheme.primaryGreen.withOpacity(0.1)
          : Colors.transparent,
        child: InkWell(
          borderRadius: BorderRadius.circular(8),
          onTap: () {
            ref.read(selectedVolunteerProvider.notifier).state = volunteer;
          },
          child: Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(8),
              border: isSelected 
                ? Border.all(color: AppTheme.primaryGreen, width: 2)
                : null,
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Name and status
                Row(
                  children: [
                    Expanded(
                      child: Text(
                        volunteer.name,
                        style: Theme.of(context).textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 8,
                        vertical: 2,
                      ),
                      decoration: BoxDecoration(
                        color: volunteer.isActive 
                          ? AppTheme.primaryGreen.withOpacity(0.2)
                          : Colors.grey.withOpacity(0.2),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Text(
                        volunteer.isActive ? 'Active' : 'Inactive',
                        style: TextStyle(
                          fontSize: 10,
                          fontWeight: FontWeight.bold,
                          color: volunteer.isActive 
                            ? AppTheme.primaryGreen
                            : Colors.grey,
                        ),
                      ),
                    ),
                  ],
                ),
                
                if (volunteer.email != null) ...[
                  const SizedBox(height: 4),
                  Row(
                    children: [
                      const Icon(Icons.email, size: 14, color: Colors.grey),
                      const SizedBox(width: 4),
                      Expanded(
                        child: Text(
                          volunteer.email!,
                          style: Theme.of(context).textTheme.bodySmall,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                    ],
                  ),
                ],
                
                if (volunteer.phone != null) ...[
                  const SizedBox(height: 2),
                  Row(
                    children: [
                      const Icon(Icons.phone, size: 14, color: Colors.grey),
                      const SizedBox(width: 4),
                      Text(
                        volunteer.phone!,
                        style: Theme.of(context).textTheme.bodySmall,
                      ),
                    ],
                  ),
                ],
                
                if (volunteer.skills != null) ...[
                  const SizedBox(height: 4),
                  Text(
                    volunteer.skills!,
                    style: Theme.of(context).textTheme.bodySmall?.copyWith(
                      color: Colors.grey[600],
                    ),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildVolunteerDetails(BuildContext context, WidgetRef ref) {
    final selectedVolunteer = ref.watch(selectedVolunteerProvider);

    return Card(
      child: selectedVolunteer == null 
        ? _buildNoSelectionState(context)
        : _buildDetailForm(context, ref, selectedVolunteer),
    );
  }

  Widget _buildNoSelectionState(BuildContext context) {
    return const Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.person_outline,
            size: 64,
            color: Colors.grey,
          ),
          SizedBox(height: 16),
          Text(
            'Select a volunteer to view details',
            style: TextStyle(
              fontSize: 16,
              color: Colors.grey,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildDetailForm(BuildContext context, WidgetRef ref, Volunteer volunteer) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header with actions
          Row(
            children: [
              const Icon(Icons.person, color: AppTheme.primaryGreen),
              const SizedBox(width: 8),
              Text(
                'Volunteer Details',
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                  fontWeight: FontWeight.bold,
                ),
              ),
              const Spacer(),
              PopupMenuButton<String>(
                onSelected: (value) {
                  switch (value) {
                    case 'edit':
                      _showEditVolunteerDialog(context, ref, volunteer);
                      break;
                    case 'delete':
                      _showDeleteConfirmation(context, ref, volunteer);
                      break;
                  }
                },
                itemBuilder: (context) => [
                  const PopupMenuItem(
                    value: 'edit',
                    child: Row(
                      children: [
                        Icon(Icons.edit),
                        SizedBox(width: 8),
                        Text('Edit'),
                      ],
                    ),
                  ),
                  const PopupMenuItem(
                    value: 'delete',
                    child: Row(
                      children: [
                        Icon(Icons.delete, color: Colors.red),
                        SizedBox(width: 8),
                        Text('Delete', style: TextStyle(color: Colors.red)),
                      ],
                    ),
                  ),
                ],
              ),
            ],
          ),
          const SizedBox(height: 16),
          const Divider(),
          const SizedBox(height: 16),

          // Basic Information
          _buildDetailSection(
            context,
            'Basic Information',
            Icons.info_outline,
            [
              _buildDetailRow('Name', volunteer.name),
              if (volunteer.email != null) _buildDetailRow('Email', volunteer.email!),
              if (volunteer.phone != null) _buildDetailRow('Phone', volunteer.phone!),
              if (volunteer.address != null) _buildDetailRow('Address', volunteer.address!),
              _buildDetailRow('Status', volunteer.isActive ? 'Active' : 'Inactive'),
              if (volunteer.dateJoined != null)
                _buildDetailRow(
                  'Date Joined',
                  DateFormat('dd/MM/yyyy').format(volunteer.dateJoined!),
                ),
            ],
          ),

          const SizedBox(height: 24),

          // Skills & Notes
          if (volunteer.skills != null || volunteer.notes != null)
            _buildDetailSection(
              context,
              'Skills & Notes',
              Icons.psychology,
              [
                if (volunteer.skills != null) _buildDetailRow('Skills', volunteer.skills!),
                if (volunteer.notes != null) _buildDetailRow('Notes', volunteer.notes!),
              ],
            ),

          const SizedBox(height: 24),

          // Visit Statistics (placeholder for now)
          _buildDetailSection(
            context,
            'Visit Statistics',
            Icons.analytics,
            [
              _buildDetailRow('Total Visits', '0'), // TODO: Calculate from database
              _buildDetailRow('This Month', '0'),   // TODO: Calculate from database
              _buildDetailRow('Last Visit', 'Never'), // TODO: Calculate from database
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildDetailSection(
    BuildContext context,
    String title,
    IconData icon,
    List<Widget> children,
  ) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Icon(icon, size: 18, color: AppTheme.primaryGreen),
            const SizedBox(width: 8),
            Text(
              title,
              style: Theme.of(context).textTheme.titleMedium?.copyWith(
                fontWeight: FontWeight.bold,
                color: AppTheme.primaryGreen,
              ),
            ),
          ],
        ),
        const SizedBox(height: 12),
        ...children,
      ],
    );
  }

  Widget _buildDetailRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 100,
            child: Text(
              '$label:',
              style: const TextStyle(
                fontWeight: FontWeight.w500,
                color: Colors.grey,
              ),
            ),
          ),
          Expanded(
            child: Text(value),
          ),
        ],
      ),
    );
  }

  Widget _buildEmptyState(BuildContext context) {
    return const Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.people_outline,
            size: 64,
            color: Colors.grey,
          ),
          SizedBox(height: 16),
          Text(
            'No volunteers found',
            style: TextStyle(
              fontSize: 16,
              color: Colors.grey,
            ),
          ),
        ],
      ),
    );
  }

  void _showAddVolunteerDialog(BuildContext context, WidgetRef ref) {
    _showVolunteerDialog(context, ref, null);
  }

  void _showEditVolunteerDialog(BuildContext context, WidgetRef ref, Volunteer volunteer) {
    _showVolunteerDialog(context, ref, volunteer);
  }

  void _showVolunteerDialog(BuildContext context, WidgetRef ref, Volunteer? volunteer) {
    final nameController = TextEditingController(text: volunteer?.name ?? '');
    final emailController = TextEditingController(text: volunteer?.email ?? '');
    final phoneController = TextEditingController(text: volunteer?.phone ?? '');
    final addressController = TextEditingController(text: volunteer?.address ?? '');
    final skillsController = TextEditingController(text: volunteer?.skills ?? '');
    final notesController = TextEditingController(text: volunteer?.notes ?? '');
    bool isActive = volunteer?.isActive ?? true;

    showDialog(
      context: context,
      builder: (context) => StatefulBuilder(
        builder: (context, setState) => AlertDialog(
          title: Text(volunteer == null ? 'Add Volunteer' : 'Edit Volunteer'),
          content: SizedBox(
            width: 400,
            child: SingleChildScrollView(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  TextField(
                    controller: nameController,
                    decoration: const InputDecoration(
                      labelText: 'Name *',
                      border: OutlineInputBorder(),
                    ),
                  ),
                  const SizedBox(height: 16),
                  TextField(
                    controller: emailController,
                    decoration: const InputDecoration(
                      labelText: 'Email',
                      border: OutlineInputBorder(),
                    ),
                  ),
                  const SizedBox(height: 16),
                  TextField(
                    controller: phoneController,
                    decoration: const InputDecoration(
                      labelText: 'Phone',
                      border: OutlineInputBorder(),
                    ),
                  ),
                  const SizedBox(height: 16),
                  TextField(
                    controller: addressController,
                    decoration: const InputDecoration(
                      labelText: 'Address',
                      border: OutlineInputBorder(),
                    ),
                  ),
                  const SizedBox(height: 16),
                  TextField(
                    controller: skillsController,
                    decoration: const InputDecoration(
                      labelText: 'Skills',
                      border: OutlineInputBorder(),
                    ),
                  ),
                  const SizedBox(height: 16),
                  TextField(
                    controller: notesController,
                    decoration: const InputDecoration(
                      labelText: 'Notes',
                      border: OutlineInputBorder(),
                    ),
                    maxLines: 3,
                  ),
                  const SizedBox(height: 16),
                  CheckboxListTile(
                    title: const Text('Active'),
                    value: isActive,
                    onChanged: (value) {
                      setState(() {
                        isActive = value ?? true;
                      });
                    },
                  ),
                ],
              ),
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('Cancel'),
            ),
            ElevatedButton(
              onPressed: () async {
                if (nameController.text.trim().isEmpty) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Name is required')),
                  );
                  return;
                }

                await _saveVolunteer(
                  context,
                  ref,
                  volunteer,
                  nameController.text.trim(),
                  emailController.text.trim().isEmpty ? null : emailController.text.trim(),
                  phoneController.text.trim().isEmpty ? null : phoneController.text.trim(),
                  addressController.text.trim().isEmpty ? null : addressController.text.trim(),
                  skillsController.text.trim().isEmpty ? null : skillsController.text.trim(),
                  notesController.text.trim().isEmpty ? null : notesController.text.trim(),
                  isActive,
                );

                Navigator.of(context).pop();
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: AppTheme.primaryGreen,
                foregroundColor: Colors.white,
              ),
              child: Text(volunteer == null ? 'Add' : 'Save'),
            ),
          ],
        ),
      ),
    );
  }

  Future<void> _saveVolunteer(
    BuildContext context,
    WidgetRef ref,
    Volunteer? existingVolunteer,
    String name,
    String? email,
    String? phone,
    String? address,
    String? skills,
    String? notes,
    bool isActive,
  ) async {
    try {
      final now = DateTime.now().toIso8601String();

      if (existingVolunteer == null) {
        // Add new volunteer
        await DatabaseHelper.instance.insertVolunteer({
          'name': name,
          'email': email,
          'phone': phone,
          'address': address,
          'skills': skills,
          'notes': notes,
          'is_active': isActive ? 1 : 0,
          'date_joined': now,
          'created_at': now,
          'updated_at': now,
        });
      } else {
        // Update existing volunteer
        await DatabaseHelper.instance.updateVolunteer({
          'id': existingVolunteer.id,
          'name': name,
          'email': email,
          'phone': phone,
          'address': address,
          'skills': skills,
          'notes': notes,
          'is_active': isActive ? 1 : 0,
          'date_joined': existingVolunteer.dateJoined,
          'updated_at': now,
        });
      }

      // Refresh the data
      ref.invalidate(volunteersProvider);

      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(existingVolunteer == null 
              ? 'Volunteer added successfully' 
              : 'Volunteer updated successfully'),
          ),
        );
      }
    } catch (e) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error saving volunteer: $e')),
        );
      }
    }
  }

  void _showDeleteConfirmation(BuildContext context, WidgetRef ref, Volunteer volunteer) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Delete Volunteer'),
        content: Text('Are you sure you want to delete "${volunteer.name}"?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () async {
              await _deleteVolunteer(context, ref, volunteer);
              Navigator.of(context).pop();
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.red,
              foregroundColor: Colors.white,
            ),
            child: const Text('Delete'),
          ),
        ],
      ),
    );
  }

  Future<void> _deleteVolunteer(BuildContext context, WidgetRef ref, Volunteer volunteer) async {
    try {
      await DatabaseHelper.instance.deleteVolunteer(volunteer.id!);

      // Clear selection if this volunteer was selected
      if (ref.read(selectedVolunteerProvider)?.id == volunteer.id) {
        ref.read(selectedVolunteerProvider.notifier).state = null;
      }

      // Refresh the data
      ref.invalidate(volunteersProvider);

      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Volunteer deleted successfully')),
        );
      }
    } catch (e) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error deleting volunteer: $e')),
        );
      }
    }
  }
}
