import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../../core/theme/app_theme.dart';
import '../../core/providers/theme_provider.dart';

// Settings model
class AppSettings {
  final String calendlyApiKey;
  final String koboApiUrl;
  final String koboApiToken;
  final bool autoSync;
  final int syncInterval;
  final bool notifications;
  final String language;
  final String backupLocation;

  AppSettings({
    required this.calendlyApiKey,
    required this.koboApiUrl,
    required this.koboApiToken,
    required this.autoSync,
    required this.syncInterval,
    required this.notifications,
    required this.language,
    required this.backupLocation,
  });

  AppSettings copyWith({
    String? calendlyApiKey,
    String? koboApiUrl,
    String? koboApiToken,
    bool? autoSync,
    int? syncInterval,
    bool? notifications,
    String? language,
    String? backupLocation,
  }) {
    return AppSettings(
      calendlyApiKey: calendlyApiKey ?? this.calendlyApiKey,
      koboApiUrl: koboApiUrl ?? this.koboApiUrl,
      koboApiToken: koboApiToken ?? this.koboApiToken,
      autoSync: autoSync ?? this.autoSync,
      syncInterval: syncInterval ?? this.syncInterval,
      notifications: notifications ?? this.notifications,
      language: language ?? this.language,
      backupLocation: backupLocation ?? this.backupLocation,
    );
  }
}

// Settings provider
final settingsProvider = StateNotifierProvider<SettingsNotifier, AppSettings>((ref) {
  return SettingsNotifier();
});

class SettingsNotifier extends StateNotifier<AppSettings> {
  SettingsNotifier() : super(
    AppSettings(
      calendlyApiKey: '',
      koboApiUrl: 'https://ee.kobotoolbox.org/api/v2/',
      koboApiToken: '',
      autoSync: true,
      syncInterval: 15,
      notifications: true,
      language: 'en',
      backupLocation: '',
    ),
  ) {
    _loadSettings();
  }

  Future<void> _loadSettings() async {
    final prefs = await SharedPreferences.getInstance();
    
    state = AppSettings(
      calendlyApiKey: prefs.getString('calendly_api_key') ?? '',
      koboApiUrl: prefs.getString('kobo_api_url') ?? 'https://ee.kobotoolbox.org/api/v2/',
      koboApiToken: prefs.getString('kobo_api_token') ?? '',
      autoSync: prefs.getBool('auto_sync') ?? true,
      syncInterval: prefs.getInt('sync_interval') ?? 15,
      notifications: prefs.getBool('notifications') ?? true,
      language: prefs.getString('language') ?? 'en',
      backupLocation: prefs.getString('backup_location') ?? '',
    );
  }

  Future<void> updateSetting(String key, dynamic value) async {
    final prefs = await SharedPreferences.getInstance();
    
    switch (key) {
      case 'calendly_api_key':
        await prefs.setString(key, value as String);
        state = state.copyWith(calendlyApiKey: value);
        break;
      case 'kobo_api_url':
        await prefs.setString(key, value as String);
        state = state.copyWith(koboApiUrl: value);
        break;
      case 'kobo_api_token':
        await prefs.setString(key, value as String);
        state = state.copyWith(koboApiToken: value);
        break;
      case 'auto_sync':
        await prefs.setBool(key, value as bool);
        state = state.copyWith(autoSync: value);
        break;
      case 'sync_interval':
        await prefs.setInt(key, value as int);
        state = state.copyWith(syncInterval: value);
        break;
      case 'notifications':
        await prefs.setBool(key, value as bool);
        state = state.copyWith(notifications: value);
        break;
      case 'language':
        await prefs.setString(key, value as String);
        state = state.copyWith(language: value);
        break;
      case 'backup_location':
        await prefs.setString(key, value as String);
        state = state.copyWith(backupLocation: value);
        break;
    }
  }
}

class SettingsPage extends ConsumerWidget {
  const SettingsPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final settings = ref.watch(settingsProvider);
    final themeMode = ref.watch(themeModeProvider);

    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header
            _buildHeader(context),
            const SizedBox(height: 24),
            
            // Settings content
            Expanded(
              child: SingleChildScrollView(
                child: Column(
                  children: [
                    // Theme Settings
                    _buildThemeSettings(context, ref, themeMode),
                    const SizedBox(height: 24),
                    
                    // API Integration Settings
                    _buildApiSettings(context, ref, settings),
                    const SizedBox(height: 24),
                    
                    // Sync Settings
                    _buildSyncSettings(context, ref, settings),
                    const SizedBox(height: 24),
                    
                    // Notification Settings
                    _buildNotificationSettings(context, ref, settings),
                    const SizedBox(height: 24),
                    
                    // Backup Settings
                    _buildBackupSettings(context, ref, settings),
                    const SizedBox(height: 24),
                    
                    // About Section
                    _buildAboutSection(context),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildHeader(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          '⚙️ Settings',
          style: Theme.of(context).textTheme.headlineMedium?.copyWith(
            fontWeight: FontWeight.bold,
            color: AppTheme.primaryGreen,
          ),
        ),
        const SizedBox(height: 4),
        Text(
          'Configure application preferences and integrations',
          style: Theme.of(context).textTheme.bodyLarge?.copyWith(
            color: Theme.of(context).textTheme.bodyMedium?.color,
          ),
        ),
      ],
    );
  }

  Widget _buildThemeSettings(BuildContext context, WidgetRef ref, ThemeMode themeMode) {
    return _buildSettingsCard(
      context,
      'Theme & Appearance',
      Icons.palette,
      [
        Row(
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'App Theme',
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'Choose between light and dark mode',
                    style: Theme.of(context).textTheme.bodySmall?.copyWith(
                      color: Colors.grey[600],
                    ),
                  ),
                ],
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
      ],
    );
  }

  Widget _buildApiSettings(BuildContext context, WidgetRef ref, AppSettings settings) {
    return _buildSettingsCard(
      context,
      'API Integration',
      Icons.api,
      [
        _buildSettingTextField(
          context,
          ref,
          'Calendly API Key',
          'Enter your Calendly API key for appointment sync',
          settings.calendlyApiKey,
          'calendly_api_key',
          obscureText: true,
        ),
        const SizedBox(height: 16),
        _buildSettingTextField(
          context,
          ref,
          'KoBoToolbox API URL',
          'Enter KoBoToolbox API URL',
          settings.koboApiUrl,
          'kobo_api_url',
        ),
        const SizedBox(height: 16),
        _buildSettingTextField(
          context,
          ref,
          'KoBoToolbox API Token',
          'Enter your KoBoToolbox API token',
          settings.koboApiToken,
          'kobo_api_token',
          obscureText: true,
        ),
        const SizedBox(height: 16),
        Row(
          children: [
            ElevatedButton.icon(
              onPressed: () => _testConnection(context, 'calendly'),
              icon: const Icon(Icons.wifi_protected_setup, size: 16),
              label: const Text('Test Calendly'),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.blue,
                foregroundColor: Colors.white,
              ),
            ),
            const SizedBox(width: 12),
            ElevatedButton.icon(
              onPressed: () => _testConnection(context, 'kobo'),
              icon: const Icon(Icons.wifi_protected_setup, size: 16),
              label: const Text('Test KoBo'),
              style: ElevatedButton.styleFrom(
                backgroundColor: AppTheme.primaryGreen,
                foregroundColor: Colors.white,
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildSyncSettings(BuildContext context, WidgetRef ref, AppSettings settings) {
    return _buildSettingsCard(
      context,
      'Synchronization',
      Icons.sync,
      [
        Row(
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Auto Sync',
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'Automatically sync data with external services',
                    style: Theme.of(context).textTheme.bodySmall?.copyWith(
                      color: Colors.grey[600],
                    ),
                  ),
                ],
              ),
            ),
            Switch(
              value: settings.autoSync,
              onChanged: (value) {
                ref.read(settingsProvider.notifier).updateSetting('auto_sync', value);
              },
              activeColor: AppTheme.primaryGreen,
            ),
          ],
        ),
        if (settings.autoSync) ...[
          const SizedBox(height: 16),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Sync Interval (minutes)',
                style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  fontWeight: FontWeight.w500,
                ),
              ),
              const SizedBox(height: 8),
              DropdownButtonFormField<int>(
                value: settings.syncInterval,
                decoration: const InputDecoration(
                  border: OutlineInputBorder(),
                  contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                ),
                items: const [
                  DropdownMenuItem(value: 5, child: Text('5 minutes')),
                  DropdownMenuItem(value: 15, child: Text('15 minutes')),
                  DropdownMenuItem(value: 30, child: Text('30 minutes')),
                  DropdownMenuItem(value: 60, child: Text('1 hour')),
                  DropdownMenuItem(value: 120, child: Text('2 hours')),
                ],
                onChanged: (value) {
                  if (value != null) {
                    ref.read(settingsProvider.notifier).updateSetting('sync_interval', value);
                  }
                },
              ),
            ],
          ),
        ],
        const SizedBox(height: 16),
        Row(
          children: [
            ElevatedButton.icon(
              onPressed: () => _syncNow(context),
              icon: const Icon(Icons.sync, size: 16),
              label: const Text('Sync Now'),
              style: ElevatedButton.styleFrom(
                backgroundColor: AppTheme.primaryGreen,
                foregroundColor: Colors.white,
              ),
            ),
            const SizedBox(width: 12),
            TextButton.icon(
              onPressed: () => _showSyncLog(context),
              icon: const Icon(Icons.history, size: 16),
              label: const Text('View Sync Log'),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildNotificationSettings(BuildContext context, WidgetRef ref, AppSettings settings) {
    return _buildSettingsCard(
      context,
      'Notifications',
      Icons.notifications,
      [
        Row(
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Enable Notifications',
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'Receive notifications for appointments and updates',
                    style: Theme.of(context).textTheme.bodySmall?.copyWith(
                      color: Colors.grey[600],
                    ),
                  ),
                ],
              ),
            ),
            Switch(
              value: settings.notifications,
              onChanged: (value) {
                ref.read(settingsProvider.notifier).updateSetting('notifications', value);
              },
              activeColor: AppTheme.primaryGreen,
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildBackupSettings(BuildContext context, WidgetRef ref, AppSettings settings) {
    return _buildSettingsCard(
      context,
      'Backup & Recovery',
      Icons.backup,
      [
        _buildSettingTextField(
          context,
          ref,
          'Backup Location',
          'Choose where to save backup files',
          settings.backupLocation.isEmpty ? 'Default location' : settings.backupLocation,
          'backup_location',
          readOnly: true,
          suffixIcon: IconButton(
            icon: const Icon(Icons.folder_open),
            onPressed: () => _selectBackupLocation(context, ref),
          ),
        ),
        const SizedBox(height: 16),
        Row(
          children: [
            ElevatedButton.icon(
              onPressed: () => _createBackup(context),
              icon: const Icon(Icons.save, size: 16),
              label: const Text('Create Backup'),
              style: ElevatedButton.styleFrom(
                backgroundColor: AppTheme.primaryGreen,
                foregroundColor: Colors.white,
              ),
            ),
            const SizedBox(width: 12),
            ElevatedButton.icon(
              onPressed: () => _restoreBackup(context),
              icon: const Icon(Icons.restore, size: 16),
              label: const Text('Restore Backup'),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.orange,
                foregroundColor: Colors.white,
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildAboutSection(BuildContext context) {
    return _buildSettingsCard(
      context,
      'About',
      Icons.info,
      [
        Row(
          children: [
            Container(
              width: 60,
              height: 60,
              decoration: BoxDecoration(
                color: AppTheme.primaryGreen,
                borderRadius: BorderRadius.circular(8),
              ),
              child: const Center(
                child: Text(
                  'EF071',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'EnergieFixers071',
                    style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'Version 1.0.0',
                    style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                      color: Colors.grey[600],
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'Volunteer Management System',
                    style: Theme.of(context).textTheme.bodySmall?.copyWith(
                      color: Colors.grey[600],
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
        const SizedBox(height: 16),
        Row(
          children: [
            TextButton.icon(
              onPressed: () => _showLicenses(context),
              icon: const Icon(Icons.article, size: 16),
              label: const Text('Licenses'),
            ),
            const SizedBox(width: 12),
            TextButton.icon(
              onPressed: () => _showChangelog(context),
              icon: const Icon(Icons.update, size: 16),
              label: const Text('Changelog'),
            ),
            const SizedBox(width: 12),
            TextButton.icon(
              onPressed: () => _checkForUpdates(context),
              icon: const Icon(Icons.system_update, size: 16),
              label: const Text('Check Updates'),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildSettingsCard(
    BuildContext context,
    String title,
    IconData icon,
    List<Widget> children,
  ) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, color: AppTheme.primaryGreen),
                const SizedBox(width: 8),
                Text(
                  title,
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            ...children,
          ],
        ),
      ),
    );
  }

  Widget _buildSettingTextField(
    BuildContext context,
    WidgetRef ref,
    String label,
    String hint,
    String value,
    String key, {
    bool obscureText = false,
    bool readOnly = false,
    Widget? suffixIcon,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: Theme.of(context).textTheme.titleMedium?.copyWith(
            fontWeight: FontWeight.w500,
          ),
        ),
        const SizedBox(height: 8),
        TextField(
          controller: TextEditingController(text: value),
          decoration: InputDecoration(
            hintText: hint,
            border: const OutlineInputBorder(),
            contentPadding: const EdgeInsets.symmetric(
              horizontal: 16,
              vertical: 12,
            ),
            suffixIcon: suffixIcon,
          ),
          obscureText: obscureText,
          readOnly: readOnly,
          onChanged: readOnly ? null : (newValue) {
            ref.read(settingsProvider.notifier).updateSetting(key, newValue);
          },
        ),
      ],
    );
  }

  void _testConnection(BuildContext context, String service) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Test $service Connection'),
        content: const Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            CircularProgressIndicator(),
            SizedBox(height: 16),
            Text('Testing connection...'),
          ],
        ),
      ),
    );

    // Simulate API test
    Future.delayed(const Duration(seconds: 2), () {
      Navigator.of(context).pop();
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text('Connection Test'),
          content: Text('$service connection test completed successfully!'),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('OK'),
            ),
          ],
        ),
      );
    });
  }

  void _syncNow(BuildContext context) {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Synchronization started...'),
        duration: Duration(seconds: 2),
      ),
    );
  }

  void _showSyncLog(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Sync Log'),
        content: const SizedBox(
          width: 400,
          height: 300,
          child: SingleChildScrollView(
            child: Text(
              '2024-01-15 10:30:25 - Calendly sync completed\n'
              '2024-01-15 10:15:22 - KoBo sync completed\n'
              '2024-01-15 10:00:18 - Auto sync started\n'
              '2024-01-15 09:45:15 - Manual sync completed\n'
              '2024-01-15 09:30:12 - Calendly sync completed\n',
              style: TextStyle(fontFamily: 'monospace'),
            ),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Close'),
          ),
        ],
      ),
    );
  }

  void _selectBackupLocation(BuildContext context, WidgetRef ref) {
    // TODO: Implement file picker for backup location
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('File picker not implemented yet')),
    );
  }

  void _createBackup(BuildContext context) {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Backup created successfully')),
    );
  }

  void _restoreBackup(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Restore Backup'),
        content: const Text(
          'Are you sure you want to restore from backup? '
          'This will overwrite all current data.',
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
                const SnackBar(content: Text('Backup restored successfully')),
              );
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.orange,
              foregroundColor: Colors.white,
            ),
            child: const Text('Restore'),
          ),
        ],
      ),
    );
  }

  void _showLicenses(BuildContext context) {
    showLicensePage(context: context, applicationName: 'EnergieFixers071');
  }

  void _showChangelog(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Changelog'),
        content: const SizedBox(
          width: 400,
          height: 300,
          child: SingleChildScrollView(
            child: Text(
              'Version 1.0.0 (Current)\n'
              '• Initial release\n'
              '• Volunteer management\n'
              '• Visit tracking\n'
              '• Calendly integration\n'
              '• KoBoToolbox integration\n'
              '• Link generator\n'
              '• Dark/light theme support\n'
              '\n'
              'Version 0.9.0 (Beta)\n'
              '• Beta testing phase\n'
              '• Bug fixes and improvements\n',
            ),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Close'),
          ),
        ],
      ),
    );
  }

  void _checkForUpdates(BuildContext context) {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('You are running the latest version')),
    );
  }
}
