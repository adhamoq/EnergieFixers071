import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/theme/app_theme.dart';

// Model for generated links
class GeneratedLink {
  final String id;
  final String title;
  final String url;
  final Map<String, String> parameters;
  final DateTime createdAt;
  final String? description;

  GeneratedLink({
    required this.id,
    required this.title,
    required this.url,
    required this.parameters,
    required this.createdAt,
    this.description,
  });
}

// Provider for generated links
final generatedLinksProvider = StateProvider<List<GeneratedLink>>((ref) => []);

// Provider for form data
final formDataProvider = StateProvider<Map<String, String>>((ref) => {});

class LinksPage extends ConsumerWidget {
  const LinksPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header
            _buildHeader(context),
            const SizedBox(height: 24),
            
            // Main content
            Expanded(
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Left panel - Link generator
                  Expanded(
                    flex: 2,
                    child: _buildLinkGenerator(context, ref),
                  ),
                  const SizedBox(width: 24),
                  
                  // Right panel - Generated links history
                  Expanded(
                    child: _buildLinksHistory(context, ref),
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
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          '🔗 Link Generator',
          style: Theme.of(context).textTheme.headlineMedium?.copyWith(
            fontWeight: FontWeight.bold,
            color: AppTheme.primaryGreen,
          ),
        ),
        const SizedBox(height: 4),
        Text(
          'Generate pre-filled forms and shareable links for energy assessments',
          style: Theme.of(context).textTheme.bodyLarge?.copyWith(
            color: Theme.of(context).textTheme.bodyMedium?.color,
          ),
        ),
      ],
    );
  }

  Widget _buildLinkGenerator(BuildContext context, WidgetRef ref) {
    final formData = ref.watch(formDataProvider);

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Generator header
            Row(
              children: [
                const Icon(Icons.auto_awesome, color: AppTheme.primaryGreen),
                const SizedBox(width: 8),
                Text(
                  'Generate Pre-filled Link',
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Text(
              'Fill out the information below to generate a pre-filled KoBoToolbox form link',
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                color: Colors.grey[600],
              ),
            ),
            const SizedBox(height: 24),
            
            // Form fields
            Expanded(
              child: SingleChildScrollView(
                child: Column(
                  children: [
                    // Basic Information Section
                    _buildSection(
                      context,
                      'Basic Information',
                      Icons.info_outline,
                      [
                        _buildTextField(
                          context,
                          ref,
                          'address',
                          'Address *',
                          'Enter the visit address',
                          formData['address'] ?? '',
                        ),
                        const SizedBox(height: 16),
                        Row(
                          children: [
                            Expanded(
                              child: _buildTextField(
                                context,
                                ref,
                                'visit_date',
                                'Visit Date',
                                'DD/MM/YYYY',
                                formData['visit_date'] ?? '',
                              ),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: _buildTextField(
                                context,
                                ref,
                                'appointment_time',
                                'Appointment Time',
                                'HH:MM',
                                formData['appointment_time'] ?? '',
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 16),
                        _buildTextField(
                          context,
                          ref,
                          'residents_count',
                          'Number of Residents',
                          'Enter number of residents',
                          formData['residents_count'] ?? '',
                        ),
                      ],
                    ),
                    
                    const SizedBox(height: 24),
                    
                    // Volunteer Information Section
                    _buildSection(
                      context,
                      'Volunteer Information',
                      Icons.people,
                      [
                        _buildTextField(
                          context,
                          ref,
                          'volunteer_name',
                          'Primary Volunteer Name',
                          'Enter volunteer name',
                          formData['volunteer_name'] ?? '',
                        ),
                        const SizedBox(height: 16),
                        _buildTextField(
                          context,
                          ref,
                          'volunteer_2_name',
                          'Secondary Volunteer Name',
                          'Enter second volunteer name (optional)',
                          formData['volunteer_2_name'] ?? '',
                        ),
                      ],
                    ),
                    
                    const SizedBox(height: 24),
                    
                    // Contact Information Section
                    _buildSection(
                      context,
                      'Contact Information',
                      Icons.contact_phone,
                      [
                        _buildTextField(
                          context,
                          ref,
                          'resident_email',
                          'Resident Email',
                          'Enter resident email',
                          formData['resident_email'] ?? '',
                        ),
                      ],
                    ),
                    
                    const SizedBox(height: 32),
                    
                    // Generate button
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton.icon(
                        onPressed: () => _generateLink(context, ref, formData),
                        icon: const Icon(Icons.link),
                        label: const Text('Generate Link'),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AppTheme.primaryGreen,
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(vertical: 16),
                          textStyle: const TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSection(
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
        const SizedBox(height: 16),
        ...children,
      ],
    );
  }

  Widget _buildTextField(
    BuildContext context,
    WidgetRef ref,
    String key,
    String label,
    String hint,
    String value,
  ) {
    return TextField(
      controller: TextEditingController(text: value),
      decoration: InputDecoration(
        labelText: label,
        hintText: hint,
        border: const OutlineInputBorder(),
        contentPadding: const EdgeInsets.symmetric(
          horizontal: 16,
          vertical: 12,
        ),
      ),
      onChanged: (newValue) {
        final currentData = ref.read(formDataProvider);
        ref.read(formDataProvider.notifier).state = {
          ...currentData,
          key: newValue,
        };
      },
    );
  }

  Widget _buildLinksHistory(BuildContext context, WidgetRef ref) {
    final generatedLinks = ref.watch(generatedLinksProvider);

    return Card(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // History header
          Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                const Icon(Icons.history, color: AppTheme.primaryGreen),
                const SizedBox(width: 8),
                Text(
                  'Generated Links',
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const Spacer(),
                Chip(
                  label: Text('${generatedLinks.length}'),
                  backgroundColor: AppTheme.primaryGreen.withOpacity(0.1),
                ),
              ],
            ),
          ),
          const Divider(height: 1),
          
          // Links list
          Expanded(
            child: generatedLinks.isEmpty
                ? _buildEmptyLinksState(context)
                : ListView.builder(
                    padding: const EdgeInsets.all(16),
                    itemCount: generatedLinks.length,
                    itemBuilder: (context, index) {
                      return _buildLinkCard(context, generatedLinks[index]);
                    },
                  ),
          ),
        ],
      ),
    );
  }

  Widget _buildEmptyLinksState(BuildContext context) {
    return const Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.link_off,
            size: 64,
            color: Colors.grey,
          ),
          SizedBox(height: 16),
          Text(
            'No links generated yet',
            style: TextStyle(
              fontSize: 16,
              color: Colors.grey,
            ),
          ),
          SizedBox(height: 8),
          Text(
            'Generate your first pre-filled link',
            style: TextStyle(
              fontSize: 12,
              color: Colors.grey,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildLinkCard(BuildContext context, GeneratedLink link) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header
            Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        link.title,
                        style: Theme.of(context).textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        'Created ${_formatDate(link.createdAt)}',
                        style: Theme.of(context).textTheme.bodySmall?.copyWith(
                          color: Colors.grey[600],
                        ),
                      ),
                    ],
                  ),
                ),
                
                // Actions
                Row(
                  children: [
                    IconButton(
                      onPressed: () => _copyLink(context, link.url),
                      icon: const Icon(Icons.copy, size: 20),
                      tooltip: 'Copy Link',
                    ),
                    IconButton(
                      onPressed: () => _shareLink(context, link),
                      icon: const Icon(Icons.share, size: 20),
                      tooltip: 'Share Link',
                    ),
                  ],
                ),
              ],
            ),
            
            const SizedBox(height: 12),
            
            // URL
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.grey[100],
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: Colors.grey[300]!),
              ),
              child: Row(
                children: [
                  Expanded(
                    child: Text(
                      link.url,
                      style: Theme.of(context).textTheme.bodySmall?.copyWith(
                        fontFamily: 'monospace',
                      ),
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                  const SizedBox(width: 8),
                  InkWell(
                    onTap: () => _copyLink(context, link.url),
                    child: const Icon(
                      Icons.copy,
                      size: 16,
                      color: AppTheme.primaryGreen,
                    ),
                  ),
                ],
              ),
            ),
            
            // Parameters summary
            if (link.parameters.isNotEmpty) ...[
              const SizedBox(height: 12),
              Wrap(
                spacing: 8,
                runSpacing: 4,
                children: link.parameters.entries.take(3).map((entry) {
                  return Chip(
                    label: Text(
                      '${entry.key}: ${entry.value}',
                      style: const TextStyle(fontSize: 10),
                    ),
                    backgroundColor: AppTheme.primaryGreen.withOpacity(0.1),
                  );
                }).toList(),
              ),
              if (link.parameters.length > 3) ...[
                const SizedBox(height: 4),
                Text(
                  '+${link.parameters.length - 3} more parameters',
                  style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    color: Colors.grey[600],
                  ),
                ),
              ],
            ],
            
            // Description
            if (link.description != null) ...[
              const SizedBox(height: 8),
              Text(
                link.description!,
                style: Theme.of(context).textTheme.bodySmall?.copyWith(
                  color: Colors.grey[600],
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  void _generateLink(BuildContext context, WidgetRef ref, Map<String, String> formData) {
    // Validate required fields
    if (formData['address']?.isEmpty ?? true) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Address is required')),
      );
      return;
    }

    // Generate the KoBoToolbox URL with parameters
    final baseUrl = 'https://ee.kobotoolbox.org/x/your-form-id'; // Replace with actual form ID
    final queryParams = <String, String>{};
    
    // Map form fields to KoBoToolbox field names
    if (formData['address']?.isNotEmpty ?? false) {
      queryParams['address'] = formData['address']!;
    }
    if (formData['visit_date']?.isNotEmpty ?? false) {
      queryParams['visit_date'] = formData['visit_date']!;
    }
    if (formData['appointment_time']?.isNotEmpty ?? false) {
      queryParams['appointment_time'] = formData['appointment_time']!;
    }
    if (formData['residents_count']?.isNotEmpty ?? false) {
      queryParams['residents_count'] = formData['residents_count']!;
    }
    if (formData['volunteer_name']?.isNotEmpty ?? false) {
      queryParams['volunteer_name'] = formData['volunteer_name']!;
    }
    if (formData['volunteer_2_name']?.isNotEmpty ?? false) {
      queryParams['volunteer_2_name'] = formData['volunteer_2_name']!;
    }
    if (formData['resident_email']?.isNotEmpty ?? false) {
      queryParams['resident_email'] = formData['resident_email']!;
    }

    // Build the URL
    final uri = Uri.parse(baseUrl).replace(queryParameters: queryParams);
    final generatedUrl = uri.toString();

    // Create the link object
    final link = GeneratedLink(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      title: 'Energy Assessment - ${formData['address'] ?? 'Unknown Address'}',
      url: generatedUrl,
      parameters: queryParams,
      createdAt: DateTime.now(),
      description: 'Pre-filled form for energy assessment visit',
    );

    // Add to history
    final currentLinks = ref.read(generatedLinksProvider);
    ref.read(generatedLinksProvider.notifier).state = [link, ...currentLinks];

    // Show success dialog with the generated link
    _showGeneratedLinkDialog(context, link);
  }

  void _showGeneratedLinkDialog(BuildContext context, GeneratedLink link) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Row(
          children: [
            Icon(Icons.check_circle, color: AppTheme.primaryGreen),
            SizedBox(width: 8),
            Text('Link Generated Successfully'),
          ],
        ),
        content: SizedBox(
          width: 500,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Your pre-filled KoBoToolbox form link has been generated:',
                style: Theme.of(context).textTheme.bodyMedium,
              ),
              const SizedBox(height: 16),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.grey[100],
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.grey[300]!),
                ),
                child: SelectableText(
                  link.url,
                  style: const TextStyle(fontFamily: 'monospace'),
                ),
              ),
              const SizedBox(height: 16),
              Text(
                'You can now share this link with residents or volunteers to pre-fill the form with the provided information.',
                style: Theme.of(context).textTheme.bodySmall?.copyWith(
                  color: Colors.grey[600],
                ),
              ),
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Close'),
          ),
          ElevatedButton.icon(
            onPressed: () {
              _copyLink(context, link.url);
              Navigator.of(context).pop();
            },
            icon: const Icon(Icons.copy),
            label: const Text('Copy Link'),
            style: ElevatedButton.styleFrom(
              backgroundColor: AppTheme.primaryGreen,
              foregroundColor: Colors.white,
            ),
          ),
        ],
      ),
    );
  }

  void _copyLink(BuildContext context, String url) {
    Clipboard.setData(ClipboardData(text: url));
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Link copied to clipboard'),
        duration: Duration(seconds: 2),
      ),
    );
  }

  void _shareLink(BuildContext context, GeneratedLink link) {
    // TODO: Implement native sharing
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Share: ${link.title}'),
        action: SnackBarAction(
          label: 'Copy',
          onPressed: () => _copyLink(context, link.url),
        ),
      ),
    );
  }

  String _formatDate(DateTime date) {
    final now = DateTime.now();
    final difference = now.difference(date);
    
    if (difference.inDays == 0) {
      return 'today';
    } else if (difference.inDays == 1) {
      return 'yesterday';
    } else if (difference.inDays < 7) {
      return '${difference.inDays} days ago';
    } else {
      return '${date.day}/${date.month}/${date.year}';
    }
  }
}
