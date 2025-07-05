import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../core/theme/app_theme.dart';

// For now, we'll use a simple model for appointments
class Appointment {
  final String id;
  final String title;
  final DateTime startTime;
  final DateTime endTime;
  final String? description;
  final String? inviteeName;
  final String? inviteeEmail;
  final String status;

  Appointment({
    required this.id,
    required this.title,
    required this.startTime,
    required this.endTime,
    this.description,
    this.inviteeName,
    this.inviteeEmail,
    this.status = 'scheduled',
  });
}

// Mock provider for appointments - in real app, this would integrate with Calendly API
final appointmentsProvider = FutureProvider<List<Appointment>>((ref) async {
  // Simulate API delay
  await Future.delayed(const Duration(milliseconds: 500));
  
  // Mock appointments data
  return [
    Appointment(
      id: '1',
      title: 'Energy Assessment Visit',
      startTime: DateTime.now().add(const Duration(days: 1, hours: 10)),
      endTime: DateTime.now().add(const Duration(days: 1, hours: 12)),
      inviteeName: 'John Doe',
      inviteeEmail: 'john.doe@example.com',
      description: 'Initial energy assessment for apartment',
    ),
    Appointment(
      id: '2',
      title: 'Follow-up Energy Visit',
      startTime: DateTime.now().add(const Duration(days: 3, hours: 14)),
      endTime: DateTime.now().add(const Duration(days: 3, hours: 16)),
      inviteeName: 'Jane Smith',
      inviteeEmail: 'jane.smith@example.com',
      description: 'Follow-up visit for energy improvements',
    ),
    Appointment(
      id: '3',
      title: 'Energy Consultation',
      startTime: DateTime.now().add(const Duration(days: 7, hours: 9)),
      endTime: DateTime.now().add(const Duration(days: 7, hours: 11)),
      inviteeName: 'Robert Johnson',
      inviteeEmail: 'robert.j@example.com',
      description: 'Initial consultation meeting',
    ),
  ];
});

// Filter providers
final selectedDateProvider = StateProvider<DateTime?>((ref) => null);
final appointmentStatusFilterProvider = StateProvider<String>((ref) => 'all');

// Filtered appointments provider
final filteredAppointmentsProvider = Provider<AsyncValue<List<Appointment>>>((ref) {
  final appointmentsAsync = ref.watch(appointmentsProvider);
  final selectedDate = ref.watch(selectedDateProvider);
  final statusFilter = ref.watch(appointmentStatusFilterProvider);
  
  return appointmentsAsync.when(
    data: (appointments) {
      var filtered = appointments;
      
      // Filter by date
      if (selectedDate != null) {
        filtered = filtered.where((appointment) {
          final appointmentDate = DateTime(
            appointment.startTime.year,
            appointment.startTime.month,
            appointment.startTime.day,
          );
          final filterDate = DateTime(
            selectedDate.year,
            selectedDate.month,
            selectedDate.day,
          );
          return appointmentDate.isAtSameMomentAs(filterDate);
        }).toList();
      }
      
      // Filter by status
      if (statusFilter != 'all') {
        filtered = filtered.where((appointment) => 
          appointment.status == statusFilter
        ).toList();
      }
      
      // Sort by start time
      filtered.sort((a, b) => a.startTime.compareTo(b.startTime));
      
      return AsyncValue.data(filtered);
    },
    loading: () => const AsyncValue.loading(),
    error: (error, stack) => AsyncValue.error(error, stack),
  );
});

class AppointmentsPage extends ConsumerWidget {
  const AppointmentsPage({Key? key}) : super(key: key);

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
            
            // Statistics and quick actions
            _buildTopSection(context, ref),
            const SizedBox(height: 24),
            
            // Filters
            _buildFilters(context, ref),
            const SizedBox(height: 24),
            
            // Appointments list
            Expanded(
              child: _buildAppointmentsList(context, ref),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildHeader(BuildContext context, WidgetRef ref) {
    return Row(
      children: [
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                '📅 Appointments Management',
                style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                  fontWeight: FontWeight.bold,
                  color: AppTheme.primaryGreen,
                ),
              ),
              const SizedBox(height: 4),
              Text(
                'Manage calendar appointments and Calendly integration',
                style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                  color: Theme.of(context).textTheme.bodyMedium?.color,
                ),
              ),
            ],
          ),
        ),
        
        // Action buttons
        Row(
          children: [
            ElevatedButton.icon(
              onPressed: () => _syncWithCalendly(context, ref),
              icon: const Icon(Icons.sync),
              label: const Text('Sync Calendar'),
              style: ElevatedButton.styleFrom(
                backgroundColor: AppTheme.primaryGreen,
                foregroundColor: Colors.white,
              ),
            ),
            const SizedBox(width: 12),
            ElevatedButton.icon(
              onPressed: () => _showCreateAppointmentDialog(context, ref),
              icon: const Icon(Icons.add),
              label: const Text('New Appointment'),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.blue,
                foregroundColor: Colors.white,
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildTopSection(BuildContext context, WidgetRef ref) {
    final appointmentsAsync = ref.watch(appointmentsProvider);

    return Row(
      children: [
        // Statistics cards
        Expanded(
          flex: 2,
          child: appointmentsAsync.when(
            data: (appointments) => _buildStatisticsCards(context, appointments),
            loading: () => const SizedBox.shrink(),
            error: (_, __) => const SizedBox.shrink(),
          ),
        ),
        
        const SizedBox(width: 24),
        
        // Calendar integration info
        Expanded(
          child: _buildCalendlyInfo(context),
        ),
      ],
    );
  }

  Widget _buildStatisticsCards(BuildContext context, List<Appointment> appointments) {
    final now = DateTime.now();
    final today = DateTime(now.year, now.month, now.day);
    final tomorrow = today.add(const Duration(days: 1));
    final nextWeek = today.add(const Duration(days: 7));

    final todayCount = appointments.where((apt) {
      final aptDate = DateTime(apt.startTime.year, apt.startTime.month, apt.startTime.day);
      return aptDate.isAtSameMomentAs(today);
    }).length;

    final tomorrowCount = appointments.where((apt) {
      final aptDate = DateTime(apt.startTime.year, apt.startTime.month, apt.startTime.day);
      return aptDate.isAtSameMomentAs(tomorrow);
    }).length;

    final nextWeekCount = appointments.where((apt) {
      final aptDate = DateTime(apt.startTime.year, apt.startTime.month, apt.startTime.day);
      return aptDate.isAfter(today) && aptDate.isBefore(nextWeek);
    }).length;

    return Row(
      children: [
        _buildStatCard(
          context,
          '📅',
          'Total',
          appointments.length.toString(),
          AppTheme.primaryGreen,
        ),
        const SizedBox(width: 16),
        _buildStatCard(
          context,
          '🕐',
          'Today',
          todayCount.toString(),
          Colors.blue,
        ),
        const SizedBox(width: 16),
        _buildStatCard(
          context,
          '⏰',
          'Tomorrow',
          tomorrowCount.toString(),
          Colors.orange,
        ),
        const SizedBox(width: 16),
        _buildStatCard(
          context,
          '📆',
          'Next 7 Days',
          nextWeekCount.toString(),
          Colors.purple,
        ),
      ],
    );
  }

  Widget _buildStatCard(
    BuildContext context,
    String icon,
    String title,
    String value,
    Color color,
  ) {
    return Expanded(
      child: Card(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Text(
                    icon,
                    style: const TextStyle(fontSize: 24),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      title,
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        color: Colors.grey[600],
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 8),
              Text(
                value,
                style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                  fontWeight: FontWeight.bold,
                  color: color,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildCalendlyInfo(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(Icons.integration_instructions, color: AppTheme.primaryGreen),
                const SizedBox(width: 8),
                Text(
                  'Calendar Integration',
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Text(
              'Sync your Calendar appointments automatically.',
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                color: Colors.grey[600],
              ),
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                Icon(
                  Icons.check_circle,
                  color: AppTheme.primaryGreen,
                  size: 16,
                ),
                const SizedBox(width: 4),
                Text(
                  'Connected',
                  style: TextStyle(
                    color: AppTheme.primaryGreen,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFilters(BuildContext context, WidgetRef ref) {
    final selectedDate = ref.watch(selectedDateProvider);
    final statusFilter = ref.watch(appointmentStatusFilterProvider);

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(Icons.filter_list, color: AppTheme.primaryGreen),
                const SizedBox(width: 8),
                Text(
                  'Filters',
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            
            Row(
              children: [
                // Date filter
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Date:'),
                      const SizedBox(height: 4),
                      InkWell(
                        onTap: () async {
                          final date = await showDatePicker(
                            context: context,
                            initialDate: selectedDate ?? DateTime.now(),
                            firstDate: DateTime.now().subtract(const Duration(days: 365)),
                            lastDate: DateTime.now().add(const Duration(days: 365)),
                          );
                          ref.read(selectedDateProvider.notifier).state = date;
                        },
                        child: Container(
                          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                          decoration: BoxDecoration(
                            border: Border.all(color: Colors.grey),
                            borderRadius: BorderRadius.circular(4),
                          ),
                          child: Row(
                            children: [
                              const Icon(Icons.calendar_today, size: 16),
                              const SizedBox(width: 8),
                              Text(
                                selectedDate != null 
                                  ? DateFormat('dd/MM/yyyy').format(selectedDate)
                                  : 'All dates',
                              ),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                
                const SizedBox(width: 16),
                
                // Status filter
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Status:'),
                      const SizedBox(height: 4),
                      DropdownButtonFormField<String>(
                        value: statusFilter,
                        decoration: const InputDecoration(
                          border: OutlineInputBorder(),
                          contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                        ),
                        items: const [
                          DropdownMenuItem(value: 'all', child: Text('All Statuses')),
                          DropdownMenuItem(value: 'scheduled', child: Text('Scheduled')),
                          DropdownMenuItem(value: 'completed', child: Text('Completed')),
                          DropdownMenuItem(value: 'cancelled', child: Text('Cancelled')),
                        ],
                        onChanged: (value) {
                          if (value != null) {
                            ref.read(appointmentStatusFilterProvider.notifier).state = value;
                          }
                        },
                      ),
                    ],
                  ),
                ),
                
                const SizedBox(width: 16),
                
                // Clear filters
                Column(
                  children: [
                    const SizedBox(height: 20),
                    ElevatedButton.icon(
                      onPressed: () {
                        ref.read(selectedDateProvider.notifier).state = null;
                        ref.read(appointmentStatusFilterProvider.notifier).state = 'all';
                      },
                      icon: const Icon(Icons.clear),
                      label: const Text('Clear'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.grey[100],
                        foregroundColor: Colors.grey[700],
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildAppointmentsList(BuildContext context, WidgetRef ref) {
    final appointmentsAsync = ref.watch(filteredAppointmentsProvider);

    return Card(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // List header
          Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                const Icon(Icons.event_note, color: AppTheme.primaryGreen),
                const SizedBox(width: 8),
                Text(
                  'Upcoming Appointments',
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ),
          const Divider(height: 1),
          
          // Appointments list
          Expanded(
            child: appointmentsAsync.when(
              data: (appointments) {
                if (appointments.isEmpty) {
                  return _buildEmptyState(context);
                }
                
                return ListView.separated(
                  padding: const EdgeInsets.all(16),
                  itemCount: appointments.length,
                  separatorBuilder: (context, index) => const SizedBox(height: 12),
                  itemBuilder: (context, index) {
                    return _buildAppointmentCard(context, appointments[index]);
                  },
                );
              },
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (error, _) => Center(
                child: Text('Error loading appointments: $error'),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildAppointmentCard(BuildContext context, Appointment appointment) {
    final isToday = _isToday(appointment.startTime);
    final isPast = appointment.startTime.isBefore(DateTime.now());

    return Card(
      elevation: 2,
      margin: EdgeInsets.zero,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header row
            Row(
              children: [
                // Time and date
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      DateFormat('HH:mm').format(appointment.startTime),
                      style: Theme.of(context).textTheme.titleLarge?.copyWith(
                        fontWeight: FontWeight.bold,
                        color: isToday ? AppTheme.primaryGreen : null,
                      ),
                    ),
                    Text(
                      DateFormat('dd/MM/yyyy').format(appointment.startTime),
                      style: Theme.of(context).textTheme.bodySmall?.copyWith(
                        color: Colors.grey[600],
                      ),
                    ),
                  ],
                ),
                
                const SizedBox(width: 16),
                
                // Appointment details
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        appointment.title,
                        style: Theme.of(context).textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      if (appointment.inviteeName != null) ...[
                        const SizedBox(height: 4),
                        Row(
                          children: [
                            const Icon(Icons.person, size: 16, color: Colors.grey),
                            const SizedBox(width: 4),
                            Text(
                              appointment.inviteeName!,
                              style: Theme.of(context).textTheme.bodyMedium,
                            ),
                          ],
                        ),
                      ],
                      if (appointment.inviteeEmail != null) ...[
                        const SizedBox(height: 2),
                        Row(
                          children: [
                            const Icon(Icons.email, size: 16, color: Colors.grey),
                            const SizedBox(width: 4),
                            Text(
                              appointment.inviteeEmail!,
                              style: Theme.of(context).textTheme.bodySmall?.copyWith(
                                color: Colors.grey[600],
                              ),
                            ),
                          ],
                        ),
                      ],
                    ],
                  ),
                ),
                
                // Status and actions
                Column(
                  crossAxisAlignment: CrossAxisAlignment.end,
                  children: [
                    _buildStatusChip(appointment.status, isPast),
                    const SizedBox(height: 8),
                    PopupMenuButton<String>(
                      onSelected: (value) => _handleAppointmentAction(context, appointment, value),
                      itemBuilder: (context) => [
                        const PopupMenuItem(
                          value: 'edit',
                          child: Row(
                            children: [
                              Icon(Icons.edit, size: 16),
                              SizedBox(width: 8),
                              Text('Edit'),
                            ],
                          ),
                        ),
                        const PopupMenuItem(
                          value: 'reschedule',
                          child: Row(
                            children: [
                              Icon(Icons.schedule, size: 16),
                              SizedBox(width: 8),
                              Text('Reschedule'),
                            ],
                          ),
                        ),
                        const PopupMenuItem(
                          value: 'cancel',
                          child: Row(
                            children: [
                              Icon(Icons.cancel, size: 16, color: Colors.red),
                              SizedBox(width: 8),
                              Text('Cancel', style: TextStyle(color: Colors.red)),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ],
            ),
            
            // Description
            if (appointment.description != null) ...[
              const SizedBox(height: 8),
              Text(
                appointment.description!,
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                  color: Colors.grey[600],
                ),
              ),
            ],
            
            // Duration
            const SizedBox(height: 8),
            Row(
              children: [
                const Icon(Icons.access_time, size: 16, color: Colors.grey),
                const SizedBox(width: 4),
                Text(
                  '${DateFormat('HH:mm').format(appointment.startTime)} - ${DateFormat('HH:mm').format(appointment.endTime)}',
                  style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    color: Colors.grey[600],
                  ),
                ),
                const SizedBox(width: 16),
                const Icon(Icons.timelapse, size: 16, color: Colors.grey),
                const SizedBox(width: 4),
                Text(
                  '${appointment.endTime.difference(appointment.startTime).inMinutes} min',
                  style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    color: Colors.grey[600],
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStatusChip(String status, bool isPast) {
    Color color;
    String displayText;
    
    if (isPast && status == 'scheduled') {
      color = Colors.red;
      displayText = 'OVERDUE';
    } else {
      switch (status) {
        case 'scheduled':
          color = Colors.blue;
          displayText = 'SCHEDULED';
          break;
        case 'completed':
          color = AppTheme.primaryGreen;
          displayText = 'COMPLETED';
          break;
        case 'cancelled':
          color = Colors.red;
          displayText = 'CANCELLED';
          break;
        default:
          color = Colors.grey;
          displayText = status.toUpperCase();
      }
    }

    return Chip(
      label: Text(
        displayText,
        style: const TextStyle(
          fontSize: 10,
          fontWeight: FontWeight.bold,
        ),
      ),
      backgroundColor: color.withOpacity(0.2),
      labelStyle: TextStyle(color: color),
    );
  }

  Widget _buildEmptyState(BuildContext context) {
    return const Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.event_busy,
            size: 64,
            color: Colors.grey,
          ),
          SizedBox(height: 16),
          Text(
            'No appointments found',
            style: TextStyle(
              fontSize: 16,
              color: Colors.grey,
            ),
          ),
        ],
      ),
    );
  }

  bool _isToday(DateTime date) {
    final now = DateTime.now();
    return date.year == now.year && 
           date.month == now.month && 
           date.day == now.day;
  }

  void _syncWithCalendly(BuildContext context, WidgetRef ref) {
    // TODO: Implement actual Calendly API integration
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Sync with Calendly'),
        content: const Text(
          'This will sync your appointments from Calendly.\n\n'
          'Note: This is a demo version. Real Calendly integration will be implemented.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.of(context).pop();
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                  content: Text('Calendly sync completed successfully'),
                ),
              );
              // Refresh appointments
              ref.invalidate(appointmentsProvider);
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: AppTheme.primaryGreen,
              foregroundColor: Colors.white,
            ),
            child: const Text('Sync'),
          ),
        ],
      ),
    );
  }

  void _showCreateAppointmentDialog(BuildContext context, WidgetRef ref) {
    // TODO: Implement create appointment dialog
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Create appointment functionality coming soon!'),
      ),
    );
  }

  void _handleAppointmentAction(BuildContext context, Appointment appointment, String action) {
    switch (action) {
      case 'edit':
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Edit appointment: ${appointment.title}')),
        );
        break;
      case 'reschedule':
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Reschedule appointment: ${appointment.title}')),
        );
        break;
      case 'cancel':
        _showCancelConfirmation(context, appointment);
        break;
    }
  }

  void _showCancelConfirmation(BuildContext context, Appointment appointment) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Cancel Appointment'),
        content: Text('Are you sure you want to cancel "${appointment.title}"?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('No'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.of(context).pop();
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('Cancelled: ${appointment.title}')),
              );
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.red,
              foregroundColor: Colors.white,
            ),
            child: const Text('Cancel Appointment'),
          ),
        ],
      ),
    );
  }
}
