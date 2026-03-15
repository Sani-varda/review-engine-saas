import 'package:flutter/material.dart';
import 'package:lucide_icons/lucide_icons.dart';
import '../services/api_service.dart';
import '../models/models.dart';
import '../theme.dart';
import 'package:intl/intl.dart';

class ReviewManagementScreen extends StatefulWidget {
  const ReviewManagementScreen({super.key});

  @override
  State<ReviewManagementScreen> createState() => _ReviewManagementScreenState();
}

class _ReviewManagementScreenState extends State<ReviewManagementScreen> {
  final _apiService = ApiService();
  List<Review> _reviews = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadReviews();
  }

  Future<void> _loadReviews() async {
    setState(() => _isLoading = true);
    final reviews = await _apiService.getReviews();
    setState(() {
      _reviews = reviews;
      _isLoading = false;
    });
  }

  void _showReplyModal(Review review) {
    final replyController = TextEditingController(text: review.reply);
    bool isGenerating = false;

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: AppTheme.surfaceColor,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      builder: (context) => StatefulBuilder(
        builder: (context, setModalState) => Padding(
          padding: EdgeInsets.only(
            bottom: MediaQuery.of(context).viewInsets.bottom,
            top: 24,
            left: 24,
            right: 24,
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Row(
                children: [
                  const Text('Reply to Review', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                  const Spacer(),
                  IconButton(onPressed: () => Navigator.pop(context), icon: const Icon(LucideIcons.x)),
                ],
              ),
              const SizedBox(height: 16),
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: AppTheme.backgroundColor,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text('"${review.comment}"', style: const TextStyle(fontStyle: FontStyle.italic)),
              ),
              const SizedBox(height: 24),
              TextField(
                controller: replyController,
                maxLines: 5,
                decoration: const InputDecoration(hintText: 'Type your reply here...'),
              ),
              const SizedBox(height: 16),
              Row(
                children: [
                  Expanded(
                    child: OutlinedButton.icon(
                      onPressed: isGenerating ? null : () async {
                        setModalState(() => isGenerating = true);
                        final aiReply = await _apiService.generateAiReply(review.comment, review.starRating);
                        if (aiReply != null) {
                          replyController.text = aiReply;
                        }
                        setModalState(() => isGenerating = false);
                      },
                      icon: const Icon(LucideIcons.sparkles, size: 18),
                      label: Text(isGenerating ? 'Generating...' : 'AI Generate'),
                      style: OutlinedButton.styleFrom(
                        foregroundColor: AppTheme.accentColor,
                        side: const BorderSide(color: AppTheme.accentColor),
                      ),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: ElevatedButton(
                      onPressed: () async {
                        final success = await _apiService.postReply(review.id, replyController.text);
                        if (mounted) {
                          Navigator.pop(context);
                          _loadReviews();
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(content: Text(success ? 'Reply posted!' : 'Failed to post reply.')),
                          );
                        }
                      },
                      child: const Text('Post Reply'),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 32),
            ],
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Manage Reviews')),
      body: RefreshIndicator(
        onRefresh: _loadReviews,
        child: _isLoading
            ? const Center(child: CircularProgressIndicator())
            : ListView.separated(
                padding: const EdgeInsets.all(16),
                itemCount: _reviews.length,
                separatorBuilder: (context, index) => const SizedBox(height: 16),
                itemBuilder: (context, index) => _buildReviewCard(_reviews[index]),
              ),
      ),
    );
  }

  Widget _buildReviewCard(Review review) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                CircleAvatar(
                  backgroundColor: AppTheme.primaryColor.withOpacity(0.2),
                  child: Text(review.reviewerName[0], style: const TextStyle(color: AppTheme.primaryColor)),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(review.reviewerName, style: const TextStyle(fontWeight: FontWeight.bold)),
                      Text(
                        DateFormat('MMM d, yyyy').format(review.createTime),
                        style: TextStyle(color: AppTheme.textSecondary, fontSize: 12),
                      ),
                    ],
                  ),
                ),
                Row(
                  children: List.generate(5, (i) => Icon(
                    LucideIcons.star,
                    size: 14,
                    color: i < review.starRating ? Colors.amber : Colors.white10,
                  )),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Text(review.comment),
            const SizedBox(height: 16),
            if (review.reply != null)
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.05),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.white.withOpacity(0.1)),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: const [
                        Icon(LucideIcons.reply, size: 12, color: AppTheme.successColor),
                        SizedBox(width: 8),
                        Text('Your Reply', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: AppTheme.successColor)),
                      ],
                    ),
                    const SizedBox(height: 4),
                    Text(review.reply!, style: TextStyle(fontSize: 13, color: AppTheme.textSecondary)),
                  ],
                ),
              ),
            const SizedBox(height: 12),
            Align(
              alignment: Alignment.centerRight,
              child: TextButton.icon(
                onPressed: () => _showReplyModal(review),
                icon: Icon(review.reply == null ? LucideIcons.messageSquare : LucideIcons.edit3, size: 16),
                label: Text(review.reply == null ? 'Reply' : 'Edit Reply'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
