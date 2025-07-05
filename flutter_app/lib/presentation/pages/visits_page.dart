import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../core/theme/app_theme.dart';
import '../../core/database/database_helper_new.dart';
import '../../data/models/visit.dart';
import '../../data/models/volunteer.dart';

// Provider for visits list
final visitsProvider = FutureProvider<List<Visit>>((ref) async {
  final maps = await DatabaseHelper.instance.getVisits();
  return List.generate(maps.length, (i) => Visit.fromMap(maps[i]));
});

// Provider for volunteers (for filter dropdown)
final volunteersForFilterProvider = FutureProvider<List<Volunteer>>((ref) async {
  final maps = await DatabaseHelper.instance.getVolunteers();
  return List.generate(maps.length, (i) => Volunteer.fromMap(maps[i]));
});

// Provider for selected visit
final selectedVisitProvider = StateProvider<Visit?>((ref) => null);

// Provider for date filters
final dateFromProvider = StateProvider<DateTime?>((ref) => null);
final dateToProvider = StateProvider<DateTime?>((ref) => null);
final volunteerFilterProvider = StateProvider<Volunteer?>((ref) => null);

// Provider for filtered visits
final filteredVisitsProvider = Provider<AsyncValue<List<Visit>>>((ref) {
  final visitsAsync = ref.watch(visitsProvider);
  final dateFrom = ref.watch(dateFromProvider);
  final dateTo = ref.watch(dateToProvider);
  final volunteerFilter = ref.watch(volunteerFilterProvider);
  
  return visitsAsync.when(
    data: (visits) {
      var filtered = visits;
      
      // Apply date filters
      if (dateFrom != null) {
        filtered = filtered.where((visit) => visit.visitDate.isAfter(dateFrom.subtract(const Duration(days: 1)))).toList();
      }
      if (dateTo != null) {
        filtered = filtered.where((visit) => visit.visitDate.isBefore(dateTo.add(const Duration(days: 1)))).toList();
      }
      
      // Apply volunteer filter
      if (volunteerFilter != null) {
        filtered = filtered.where((visit) => 
          visit.volunteerId == volunteerFilter.id || 
          visit.volunteer2Id == volunteerFilter.id
        ).toList();
      }
      
      return AsyncValue.data(filtered);
    },
    loading: () => const AsyncValue.loading(),
    error: (error, stack) => AsyncValue.error(error, stack),
  );
});

class VisitsPage extends ConsumerWidget {
  const VisitsPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header with statistics
            _buildHeader(context, ref),
            const SizedBox(height: 24),
            
            // Filters
            _buildFilters(context, ref),
            const SizedBox(height: 24),
            
            // Visits table
            Expanded(
              child: _buildVisitsTable(context, ref),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildHeader(BuildContext context, WidgetRef ref) {
    final visitsAsync = ref.watch(visitsProvider);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Title
        Row(
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    '🏠 Energy Visits Management',
                    style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                      color: AppTheme.primaryGreen,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'Track and manage energy assessment visits',
                    style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                      color: Theme.of(context).textTheme.bodyMedium?.color,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
        
        const SizedBox(height: 16),
        
        // Statistics cards
        visitsAsync.when(
          data: (visits) => _buildStatisticsCards(context, visits),
          loading: () => const SizedBox.shrink(),
          error: (_, __) => const SizedBox.shrink(),
        ),
      ],
    );
  }

  Widget _buildStatisticsCards(BuildContext context, List<Visit> visits) {
    final now = DateTime.now();
    final thisMonth = visits.where((visit) => 
      visit.visitDate.year == now.year && 
      visit.visitDate.month == now.month
    ).length;
    
    final withIssues = visits.where((visit) => 
      visit.moldIssues || visit.moistureIssues || visit.draftIssues
    ).length;
    
    final avgResidents = visits.isEmpty ? 0.0 : 
      visits.map((v) => v.residentsCount).reduce((a, b) => a + b) / visits.length;

    return Row(
      children: [
        _buildStatCard(
          context,
          '🏠',
          'Total Visits',
          visits.length.toString(),
          AppTheme.primaryGreen,
        ),
        const SizedBox(width: 16),
        _buildStatCard(
          context,
          '📅',
          'This Month',
          thisMonth.toString(),
          Colors.blue,
        ),
        const SizedBox(width: 16),
        _buildStatCard(
          context,
          '⚠️',
          'With Issues',
          withIssues.toString(),
          Colors.orange,
        ),
        const SizedBox(width: 16),
        _buildStatCard(
          context,
          '👥',
          'Avg Residents',
          avgResidents.toStringAsFixed(1),
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

  Widget _buildFilters(BuildContext context, WidgetRef ref) {
    final volunteersAsync = ref.watch(volunteersForFilterProvider);
    final dateFrom = ref.watch(dateFromProvider);
    final dateTo = ref.watch(dateToProvider);
    final volunteerFilter = ref.watch(volunteerFilterProvider);

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
                // Date from
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('From Date:'),
                      const SizedBox(height: 4),
                      InkWell(
                        onTap: () async {
                          final date = await showDatePicker(
                            context: context,
                            initialDate: dateFrom ?? DateTime.now(),
                            firstDate: DateTime(2020),
                            lastDate: DateTime.now().add(const Duration(days: 365)),
                          );
                          if (date != null) {
                            ref.read(dateFromProvider.notifier).state = date;
                          }
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
                                dateFrom != null 
                                  ? DateFormat('dd/MM/yyyy').format(dateFrom)
                                  : 'Select date',
                              ),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                
                const SizedBox(width: 16),
                
                // Date to
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('To Date:'),
                      const SizedBox(height: 4),
                      InkWell(
                        onTap: () async {
                          final date = await showDatePicker(
                            context: context,
                            initialDate: dateTo ?? DateTime.now(),
                            firstDate: DateTime(2020),
                            lastDate: DateTime.now().add(const Duration(days: 365)),
                          );
                          if (date != null) {
                            ref.read(dateToProvider.notifier).state = date;
                          }
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
                                dateTo != null 
                                  ? DateFormat('dd/MM/yyyy').format(dateTo)
                                  : 'Select date',
                              ),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                
                const SizedBox(width: 16),
                
                // Volunteer filter
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Volunteer:'),
                      const SizedBox(height: 4),
                      volunteersAsync.when(
                        data: (volunteers) => DropdownButtonFormField<Volunteer>(
                          value: volunteerFilter,
                          decoration: const InputDecoration(
                            border: OutlineInputBorder(),
                            contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                          ),
                          hint: const Text('All Volunteers'),
                          items: [
                            const DropdownMenuItem<Volunteer>(
                              value: null,
                              child: Text('All Volunteers'),
                            ),
                            ...volunteers.map((volunteer) => DropdownMenuItem<Volunteer>(
                              value: volunteer,
                              child: Text(volunteer.name),
                            )),
                          ],
                          onChanged: (volunteer) {
                            ref.read(volunteerFilterProvider.notifier).state = volunteer;
                          },
                        ),
                        loading: () => const SizedBox(height: 40),
                        error: (_, __) => const SizedBox(height: 40),
                      ),
                    ],
                  ),
                ),
                
                const SizedBox(width: 16),
                
                // Clear filters button
                Column(
                  children: [
                    const SizedBox(height: 20),
                    ElevatedButton.icon(
                      onPressed: () {
                        ref.read(dateFromProvider.notifier).state = null;
                        ref.read(dateToProvider.notifier).state = null;
                        ref.read(volunteerFilterProvider.notifier).state = null;
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

  Widget _buildVisitsTable(BuildContext context, WidgetRef ref) {
    final visitsAsync = ref.watch(filteredVisitsProvider);

    return Card(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Table header
          Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                const Icon(Icons.table_chart, color: AppTheme.primaryGreen),
                const SizedBox(width: 8),
                Text(
                  'Visit Records',
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ),
          const Divider(height: 1),
          
          // Table content
          Expanded(
            child: visitsAsync.when(
              data: (visits) {
                if (visits.isEmpty) {
                  return _buildEmptyState(context);
                }
                
                return SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: DataTable(
                    columns: const [
                      DataColumn(label: Text('Date')),
                      DataColumn(label: Text('Address')),
                      DataColumn(label: Text('Primary Volunteer')),
                      DataColumn(label: Text('Secondary Volunteer')),
                      DataColumn(label: Text('Residents')),
                      DataColumn(label: Text('Issues')),
                      DataColumn(label: Text('Status')),
                      DataColumn(label: Text('Actions')),
                    ],
                    rows: visits.map((visit) => _buildVisitRow(context, ref, visit)).toList(),
                  ),
                );
              },
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (error, _) => Center(
                child: Text('Error loading visits: $error'),
              ),
            ),
          ),
        ],
      ),
    );
  }

  DataRow _buildVisitRow(BuildContext context, WidgetRef ref, Visit visit) {
    // Get issues summary
    List<String> issues = [];
    if (visit.moldIssues) issues.add('Mold');
    if (visit.moistureIssues) issues.add('Moisture');
    if (visit.draftIssues) issues.add('Draft');
    final issuesText = issues.isEmpty ? 'None' : issues.join(', ');

    return DataRow(
      cells: [
        DataCell(Text(DateFormat('dd/MM/yyyy').format(visit.visitDate))),
        DataCell(
          ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 200),
            child: Text(
              visit.address,
              overflow: TextOverflow.ellipsis,
            ),
          ),
        ),
        DataCell(Text('Volunteer ${visit.volunteerId ?? "Unknown"}')), // TODO: Get actual volunteer name
        DataCell(Text(visit.volunteer2Id != null ? 'Volunteer ${visit.volunteer2Id}' : 'None')),
        DataCell(Text(visit.residentsCount.toString())),
        DataCell(
          Chip(
            label: Text(
              issuesText,
              style: const TextStyle(fontSize: 12),
            ),
            backgroundColor: issues.isNotEmpty 
              ? Colors.orange.withOpacity(0.2)
              : Colors.green.withOpacity(0.2),
          ),
        ),
        DataCell(
          Chip(
            label: Text(
              visit.status.toUpperCase(),
              style: const TextStyle(fontSize: 12),
            ),
            backgroundColor: _getStatusColor(visit.status).withOpacity(0.2),
          ),
        ),
        DataCell(
          IconButton(
            icon: const Icon(Icons.visibility, size: 18),
            onPressed: () => _showVisitDetails(context, visit),
            tooltip: 'View Details',
          ),
        ),
      ],
    );
  }

  Color _getStatusColor(String status) {
    switch (status.toLowerCase()) {
      case 'completed':
        return Colors.green;
      case 'pending':
        return Colors.orange;
      case 'cancelled':
        return Colors.red;
      default:
        return Colors.grey;
    }
  }

  Widget _buildEmptyState(BuildContext context) {
    return const Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.home_work_outlined,
            size: 64,
            color: Colors.grey,
          ),
          SizedBox(height: 16),
          Text(
            'No visits found',
            style: TextStyle(
              fontSize: 16,
              color: Colors.grey,
            ),
          ),
        ],
      ),
    );
  }

  void _showVisitDetails(BuildContext context, Visit visit) {
    showDialog(
      context: context,
      builder: (context) => Dialog(
        child: Container(
          width: 800,
          height: 600,
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header
              Row(
                children: [
                  Expanded(
                    child: Text(
                      'Visit Details',
                      style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                        fontWeight: FontWeight.bold,
                        color: AppTheme.primaryGreen,
                      ),
                    ),
                  ),
                  IconButton(
                    onPressed: () => Navigator.of(context).pop(),
                    icon: const Icon(Icons.close),
                  ),
                ],
              ),
              const Divider(),
              const SizedBox(height: 16),
              
              // Visit details
              Expanded(
                child: SingleChildScrollView(
                  child: _buildVisitDetailsContent(context, visit),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildVisitDetailsContent(BuildContext context, Visit visit) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Basic Information
        _buildDetailSection(
          context,
          'Basic Information',
          Icons.info_outline,
          [
            _buildDetailRow('Date', DateFormat('dd/MM/yyyy').format(visit.visitDate)),
            _buildDetailRow('Address', visit.address),
            if (visit.appointmentTime != null) 
              _buildDetailRow('Appointment Time', visit.appointmentTime!),
            _buildDetailRow('Residents Count', visit.residentsCount.toString()),
            _buildDetailRow('Status', visit.status.toUpperCase()),
          ],
        ),
        
        const SizedBox(height: 24),
        
        // Energy Assessment
        _buildDetailSection(
          context,
          'Energy Assessment',
          Icons.energy_savings_leaf,
          [
            _buildDetailRow('Energy Measures Taken', visit.energyMeasuresTaken ? 'Yes' : 'No'),
            if (visit.whichMeasures != null)
              _buildDetailRow('Which Measures', visit.whichMeasures!),
            _buildDetailRow('Ventilation Checked', visit.ventilationChecked ? 'Yes' : 'No'),
            _buildDetailRow('Energy Usage Checked', visit.energyUsageChecked ? 'Yes' : 'No'),
          ],
        ),
        
        const SizedBox(height: 24),
        
        // Materials & Interventions
        _buildDetailSection(
          context,
          'Materials & Interventions',
          Icons.build,
          [
            if (visit.radiatorFoilMeters > 0)
              _buildDetailRow('Radiator Foil', '${visit.radiatorFoilMeters}m'),
            if (visit.draftStripMeters > 0)
              _buildDetailRow('Draft Strip', '${visit.draftStripMeters}m'),
            if (visit.e14LedsCount > 0)
              _buildDetailRow('E14 LEDs', visit.e14LedsCount.toString()),
            if (visit.e27LedsCount > 0)
              _buildDetailRow('E27 LEDs', visit.e27LedsCount.toString()),
          ],
        ),
        
        const SizedBox(height: 24),
        
        // Issues
        if (visit.moldIssues || visit.moistureIssues || visit.draftIssues) ...[
          _buildDetailSection(
            context,
            'Issues Identified',
            Icons.warning,
            [
              if (visit.moldIssues) _buildDetailRow('Mold Issues', 'Yes'),
              if (visit.moistureIssues) _buildDetailRow('Moisture Issues', 'Yes'),
              if (visit.draftIssues) _buildDetailRow('Draft Issues', 'Yes'),
              if (visit.problemsWith != null)
                _buildDetailRow('Problems Description', visit.problemsWith!),
            ],
          ),
          const SizedBox(height: 24),
        ],
        
        // Additional Notes
        if (visit.otherRemarks != null) ...[
          _buildDetailSection(
            context,
            'Additional Remarks',
            Icons.note,
            [
              _buildDetailRow('Notes', visit.otherRemarks!),
            ],
          ),
        ],
      ],
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
            width: 150,
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
}
