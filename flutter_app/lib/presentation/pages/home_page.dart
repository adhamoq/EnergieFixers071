import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../core/theme/app_theme.dart';

class HomePage extends ConsumerWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header section
            _buildHeader(context),
            const SizedBox(height: 24),
            
            // Statistics cards
            _buildStatisticsCards(context),
            const SizedBox(height: 24),
            
            // Content sections
            Expanded(
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Left column - Recent activity
                  Expanded(
                    flex: 2,
                    child: _buildRecentActivity(context),
                  ),
                  const SizedBox(width: 24),
                  
                  // Right column - Quick actions
                  Expanded(
                    flex: 1,
                    child: _buildQuickActions(context),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildHeader(BuildContext context) {
    final now = DateTime.now();
    final dateFormat = DateFormat('EEEE, MMMM d, yyyy');
    
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Welcome to EnergieFixers071',
          style: Theme.of(context).textTheme.headlineLarge?.copyWith(
            color: AppTheme.primaryGreen,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 8),
        Text(
          dateFormat.format(now),
          style: Theme.of(context).textTheme.bodyLarge?.copyWith(
            color: Theme.of(context).textTheme.bodyLarge?.color?.withOpacity(0.7),
          ),
        ),
      ],
    );
  }

  Widget _buildStatisticsCards(BuildContext context) {
    // In a real app, these would come from providers/repositories
    final stats = [
      StatCard(
        icon: Icons.people,
        title: 'Total Volunteers',
        value: '24',
        color: AppTheme.primaryGreen,
        trend: '+2 this month',
      ),
      StatCard(
        icon: Icons.check_circle,
        title: 'Active Volunteers',
        value: '20',
        color: AppTheme.lightSuccess,
        trend: '+1 this week',
      ),
      StatCard(
        icon: Icons.home_work,
        title: 'Total Visits',
        value: '156',
        color: AppTheme.lightInfo,
        trend: '+8 this month',
      ),
      StatCard(
        icon: Icons.calendar_today,
        title: 'This Month',
        value: '12',
        color: AppTheme.lightWarning,
        trend: '3 scheduled',
      ),
    ];

    return Row(
      children: stats.map((stat) {
        return Expanded(
          child: Padding(
            padding: const EdgeInsets.only(right: 16),
            child: _buildStatCard(context, stat),
          ),
        );
      }).toList(),
    );
  }

  Widget _buildStatCard(BuildContext context, StatCard stat) {
    return Card(
      elevation: 2,
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    color: stat.color.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Icon(
                    stat.icon,
                    color: stat.color,
                    size: 24,
                  ),
                ),
                const Spacer(),
                Icon(
                  Icons.trending_up,
                  color: stat.color,
                  size: 16,
                ),
              ],
            ),
            const SizedBox(height: 16),
            Text(
              stat.value,
              style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                fontWeight: FontWeight.bold,
                color: stat.color,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              stat.title,
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                fontWeight: FontWeight.w500,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              stat.trend,
              style: Theme.of(context).textTheme.bodySmall?.copyWith(
                color: Theme.of(context).textTheme.bodySmall?.color?.withOpacity(0.6),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildRecentActivity(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(
                  Icons.history,
                  color: AppTheme.primaryGreen,
                ),
                const SizedBox(width: 8),
                Text(
                  'Recent Activity',
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Expanded(
              child: ListView(
                children: [
                  _buildActivityItem(
                    context,
                    'Visit completed at Cornelis Schuytlaan 25',
                    'Sarah van der Berg • 2 hours ago',
                    Icons.home_work,
                    AppTheme.lightSuccess,
                  ),
                  _buildActivityItem(
                    context,
                    'New volunteer registration',
                    'Adham Al Moqdad • 5 hours ago',
                    Icons.person_add,
                    AppTheme.lightInfo,
                  ),
                  _buildActivityItem(
                    context,
                    'Appointment scheduled',
                    'Weidehof 15, Utrecht • Yesterday',
                    Icons.calendar_today,
                    AppTheme.lightWarning,
                  ),
                  _buildActivityItem(
                    context,
                    'Link generated for new visit',
                    'Patricia Santos • 2 days ago',
                    Icons.link,
                    AppTheme.primaryGreen,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildActivityItem(
    BuildContext context,
    String title,
    String subtitle,
    IconData icon,
    Color color,
  ) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: color.withOpacity(0.1),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Icon(
              icon,
              color: color,
              size: 20,
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    fontWeight: FontWeight.w500,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  subtitle,
                  style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    color: Theme.of(context).textTheme.bodySmall?.color?.withOpacity(0.6),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildQuickActions(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(
                  Icons.flash_on,
                  color: AppTheme.primaryGreen,
                ),
                const SizedBox(width: 8),
                Text(
                  'Quick Actions',
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Expanded(
              child: Column(
                children: [
                  _buildQuickActionButton(
                    context,
                    'Add New Volunteer',
                    'Register a new team member',
                    Icons.person_add,
                    AppTheme.lightSuccess,
                    () {
                      // Navigate to volunteers page
                    },
                  ),
                  const SizedBox(height: 12),
                  _buildQuickActionButton(
                    context,
                    'Schedule Visit',
                    'Plan a new energy assessment',
                    Icons.calendar_today,
                    AppTheme.lightInfo,
                    () {
                      // Navigate to appointments page
                    },
                  ),
                  const SizedBox(height: 12),
                  _buildQuickActionButton(
                    context,
                    'Generate Link',
                    'Create pre-filled form link',
                    Icons.link,
                    AppTheme.lightWarning,
                    () {
                      // Navigate to links page
                    },
                  ),
                  const SizedBox(height: 12),
                  _buildQuickActionButton(
                    context,
                    'View Reports',
                    'Analytics and insights',
                    Icons.analytics,
                    AppTheme.primaryGreen,
                    () {
                      // Show reports dialog
                    },
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildQuickActionButton(
    BuildContext context,
    String title,
    String subtitle,
    IconData icon,
    Color color,
    VoidCallback onTap,
  ) {
    return SizedBox(
      width: double.infinity,
      child: ElevatedButton(
        onPressed: onTap,
        style: ElevatedButton.styleFrom(
          backgroundColor: color.withOpacity(0.1),
          foregroundColor: color,
          elevation: 0,
          padding: const EdgeInsets.all(16),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
        child: Row(
          children: [
            Icon(icon, size: 24),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                      fontWeight: FontWeight.w600,
                      color: color,
                    ),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    subtitle,
                    style: Theme.of(context).textTheme.bodySmall?.copyWith(
                      color: color.withOpacity(0.7),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class StatCard {
  final IconData icon;
  final String title;
  final String value;
  final Color color;
  final String trend;

  const StatCard({
    required this.icon,
    required this.title,
    required this.value,
    required this.color,
    required this.trend,
  });
}
