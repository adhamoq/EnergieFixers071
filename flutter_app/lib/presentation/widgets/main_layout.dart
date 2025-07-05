import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/providers/theme_provider.dart';
import '../../core/theme/app_theme.dart';

class MainLayout extends ConsumerWidget {
  final Widget child;

  const MainLayout({
    Key? key,
    required this.child,
  }) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      body: Row(
        children: [
          // Sidebar (matching your Python app's sidebar)
          _buildSidebar(context, ref),
          
          // Main content area
          Expanded(
            child: child,
          ),
        ],
      ),
    );
  }

  Widget _buildSidebar(BuildContext context, WidgetRef ref) {
    final currentLocation = GoRouterState.of(context).uri.toString();
    
    return Container(
      width: 300, // Same as your Python app's SIDEBAR_WIDTH
      decoration: BoxDecoration(
        color: Theme.of(context).drawerTheme.backgroundColor,
        border: Border(
          right: BorderSide(
            color: Theme.of(context).dividerColor,
            width: 1,
          ),
        ),
      ),
      
      child: Column(
        children: [
          // Header with logo
          _buildSidebarHeader(context),
          
          // Navigation items
          Expanded(
            child: _buildNavigationItems(context, currentLocation),
          ),
          
          // Theme toggle (in footer)
          _buildSidebarFooter(context, ref),
        ],
      ),
    );
  }

  Widget _buildSidebarHeader(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(20),
      child: Column(
        children: [
          // Your actual logo
          const Image(
            image: AssetImage('assets/images/Logo-Energiefixers071.png'),
            width: 120,
            height: 80,
          ),
          const SizedBox(height: 10),
          Text(
            'EnergieFixers071',
            style: Theme.of(context).textTheme.titleLarge?.copyWith(
              fontWeight: FontWeight.bold,
              color: AppTheme.primaryGreen,
            ),
          ),
          const SizedBox(height: 5),
          Text(
            'Volunteer Management',
            style: Theme.of(context).textTheme.bodySmall?.copyWith(
              color: Theme.of(context).textTheme.bodySmall?.color?.withOpacity(0.7),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildNavigationItems(BuildContext context, String currentLocation) {
    final navigationItems = [
      NavigationItem(
        icon: Icons.home,
        label: 'Dashboard',
        description: 'Overview & Statistics',
        route: '/',
      ),
      NavigationItem(
        icon: Icons.people,
        label: 'Volunteers',
        description: 'Manage Volunteer Data',
        route: '/volunteers',
      ),
      NavigationItem(
        icon: Icons.calendar_today,
        label: 'Appointments',
        description: 'Calendar & Scheduling',
        route: '/appointments',
      ),
      NavigationItem(
        icon: Icons.home_work,
        label: 'Visits',
        description: 'Energy Assessment Records',
        route: '/visits',
      ),
      NavigationItem(
        icon: Icons.link,
        label: 'Link Generator',
        description: 'Create Pre-filled Forms',
        route: '/links',
      ),
      NavigationItem(
        icon: Icons.settings,
        label: 'Settings',
        description: 'App Configuration',
        route: '/settings',
      ),
    ];

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 15),
      child: Column(
        children: navigationItems.map((item) {
          final isActive = currentLocation == item.route;
          
          return Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: _buildNavigationButton(
              context, 
              item, 
              isActive,
            ),
          );
        }).toList(),
      ),
    );
  }

  Widget _buildNavigationButton(
    BuildContext context, 
    NavigationItem item, 
    bool isActive,
  ) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        SizedBox(
          width: double.infinity,
          child: ElevatedButton.icon(
            onPressed: () => context.go(item.route),
            icon: Icon(item.icon, size: 20),
            label: Text(item.label),
            style: ElevatedButton.styleFrom(
              backgroundColor: isActive 
                ? AppTheme.primaryGreen 
                : Theme.of(context).cardColor,
              foregroundColor: isActive 
                ? Colors.white 
                : Theme.of(context).textTheme.bodyLarge?.color,
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              alignment: Alignment.centerLeft,
              elevation: isActive ? 2 : 0,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(8),
              ),
            ),
          ),
        ),
        Padding(
          padding: const EdgeInsets.only(left: 12, top: 2),
          child: Text(
            item.description,
            style: Theme.of(context).textTheme.bodySmall?.copyWith(
              color: Theme.of(context).textTheme.bodySmall?.color?.withOpacity(0.6),
              fontSize: 10,
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildSidebarFooter(BuildContext context, WidgetRef ref) {
    final themeMode = ref.watch(themeModeProvider);
    
    return Container(
      padding: const EdgeInsets.all(20),
      child: Column(
        children: [
          const Divider(),
          const SizedBox(height: 10),
          
          // Theme toggle (moved from settings to sidebar footer)
          Row(
            children: [
              Icon(
                themeMode == ThemeMode.dark ? Icons.dark_mode : Icons.light_mode,
                size: 20,
                color: Theme.of(context).textTheme.bodyMedium?.color,
              ),
              const SizedBox(width: 10),
              Expanded(
                child: Text(
                  themeMode == ThemeMode.dark ? 'Dark Mode' : 'Light Mode',
                  style: Theme.of(context).textTheme.bodyMedium,
                ),
              ),
              Switch(
                value: themeMode == ThemeMode.dark,
                onChanged: (value) {
                  ref.read(themeModeProvider.notifier).setTheme(
                    value ? ThemeMode.dark : ThemeMode.light,
                  );
                },
                activeColor: AppTheme.primaryGreen,
              ),
            ],
          ),
          
          const SizedBox(height: 10),
          Text(
            'v1.0.0',
            style: Theme.of(context).textTheme.bodySmall?.copyWith(
              color: Theme.of(context).textTheme.bodySmall?.color?.withOpacity(0.5),
            ),
          ),
        ],
      ),
    );
  }
}

class NavigationItem {
  final IconData icon;
  final String label;
  final String description;
  final String route;

  const NavigationItem({
    required this.icon,
    required this.label,
    required this.description,
    required this.route,
  });
}
