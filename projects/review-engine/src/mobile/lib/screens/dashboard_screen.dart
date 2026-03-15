import 'package:flutter/material.dart';
import 'package:lucide_icons/lucide_icons.dart';
import '../services/api_service.dart';
import '../models/models.dart';
import '../theme.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  final _apiService = ApiService();
  DashboardStats? _stats;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadStats();
  }

  Future<void> _loadStats() async {
    setState(() => _isLoading = true);
    final stats = await _apiService.getStats();
    setState(() {
      _stats = stats;
      _isLoading = false;
    });
  }

  void _showRequestDialog() {
    final nameController = TextEditingController();
    final contactController = TextEditingController();

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Send Review Request'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              controller: nameController,
              decoration: const InputDecoration(hintText: 'Customer Name'),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: contactController,
              decoration: const InputDecoration(hintText: 'Email or Phone'),
            ),
          ],
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text('Cancel')),
          ElevatedButton(
            onPressed: () async {
              final success = await _apiService.sendReviewRequest(
                nameController.text,
                contactController.text,
              );
              if (mounted) {
                Navigator.pop(context);
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text(success ? 'Request sent!' : 'Failed to send request.')),
                );
              }
            },
            child: const Text('Send'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Dashboard', style: TextStyle(fontWeight: FontWeight.bold)),
        backgroundColor: Colors.transparent,
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(LucideIcons.logOut),
            onPressed: () async {
              await _apiService.logout();
              if (mounted) Navigator.pushReplacementNamed(context, '/login');
            },
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: _loadStats,
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          physics: const AlwaysScrollableScrollPhysics(),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              _buildStatsGrid(),
              const SizedBox(height: 32),
              _buildActionButton(
                'Send Review Request',
                LucideIcons.send,
                AppTheme.primaryColor,
                _showRequestDialog,
              ),
              const SizedBox(height: 16),
              _buildActionButton(
                'Manage Reviews',
                LucideIcons.messageSquare,
                AppTheme.secondaryColor,
                () => Navigator.pushNamed(context, '/reviews'),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildStatsGrid() {
    if (_isLoading) {
      return const Center(child: CircularProgressIndicator());
    }

    if (_stats == null) {
      return Center(
        child: Column(
          children: [
            const Icon(LucideIcons.alertTriangle, color: Colors.orange, size: 48),
            const SizedBox(height: 16),
            const Text('Failed to load dashboard data.', style: TextStyle(color: Colors.white70)),
            TextButton(onPressed: _loadStats, child: const Text('Retry')),
          ],
        ),
      );
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        GridView.count(
          crossAxisCount: 2,
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          mainAxisSpacing: 16,
          crossAxisSpacing: 16,
          childAspectRatio: 1.2,
          children: [
            _buildStatCard('Avg Rating', _stats?.averageRating.toStringAsFixed(1) ?? '0.0', LucideIcons.star, Colors.amber),
            _buildStatCard('Requests', _stats?.totalRequests.toString() ?? '0', LucideIcons.send, Colors.blue),
            _buildStatCard('Reviews', _stats?.completedReviews.toString() ?? '0', LucideIcons.checkCircle, Colors.green),
            _buildStatCard('Conversion', '${_stats?.conversionRate.toStringAsFixed(1) ?? "0.0"}%', LucideIcons.trendingUp, Colors.violet),
          ],
        ),
        const SizedBox(height: 24),
        _buildAutoReplyToggle(),
      ],
    );
  }

  Widget _buildAutoReplyToggle() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
      decoration: BoxDecoration(
        color: AppTheme.surfaceColor,
        borderRadius: BorderRadius.circular(16),
      ),
      child: Row(
        children: [
          const Icon(LucideIcons.bot, color: Colors.blue),
          const SizedBox(width: 16),
          const Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('AI Auto-Reply', style: TextStyle(fontWeight: FontWeight.bold)),
                Text('Post replies automatically', style: TextStyle(fontSize: 12, color: Colors.white54)),
              ],
            ),
          ),
          Switch(
            value: _stats?.autoReplyEnabled ?? false,
            onChanged: (val) async {
              final success = await _apiService.toggleAutoReply(val);
              if (success) {
                _loadStats();
              }
            },
          ),
        ],
      ),
    );
  }

  Widget _buildStatCard(String label, String value, IconData icon, Color color) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, color: color, size: 24),
            const SizedBox(height: 12),
            Text(value, style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
            Text(label, style: TextStyle(color: AppTheme.textSecondary, fontSize: 12)),
          ],
        ),
      ),
    );
  }

  Widget _buildActionButton(String label, IconData icon, Color color, VoidCallback onTap) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(16),
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 20, horizontal: 24),
        decoration: BoxDecoration(
          color: color.withOpacity(0.1),
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: color.withOpacity(0.3)),
        ),
        child: Row(
          children: [
            Icon(icon, color: color),
            const SizedBox(width: 16),
            Text(label, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w600)),
            const Spacer(),
            Icon(LucideIcons.chevronRight, color: AppTheme.textSecondary, size: 20),
          ],
        ),
      ),
    );
  }
}
