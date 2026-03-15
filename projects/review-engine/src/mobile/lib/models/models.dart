class User {
  final int id;
  final String email;
  final String? name;

  User({required this.id, required this.email, this.name});

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      email: json['email'],
      name: json['name'],
    );
  }
}

class Review {
  final String id;
  final String reviewerName;
  final String comment;
  final int starRating;
  final DateTime createTime;
  final String? reply;

  Review({
    required this.id,
    required this.reviewerName,
    required this.comment,
    required this.starRating,
    required this.createTime,
    this.reply,
  });

  factory Review.fromJson(Map<String, dynamic> json) {
    return Review(
      id: json['name'] ?? '',
      reviewerName: json['reviewer']['displayName'] ?? 'Anonymous',
      comment: json['comment'] ?? '',
      starRating: _parseStarRating(json['starRating']),
      createTime: DateTime.parse(json['createTime']),
      reply: json['reviewReply']?['comment'],
    );
  }

  static int _parseStarRating(dynamic rating) {
    if (rating == 'FIVE') return 5;
    if (rating == 'FOUR') return 4;
    if (rating == 'THREE') return 3;
    if (rating == 'TWO') return 2;
    if (rating == 'ONE') return 1;
    return 0;
  }
}

class DashboardStats {
  final double averageRating;
  final int totalReviews;
  final int pendingReplies;

  DashboardStats({
    required this.averageRating,
    required this.totalReviews,
    required this.pendingReplies,
  });

  factory DashboardStats.fromJson(Map<String, dynamic> json) {
    return DashboardStats(
      averageRating: json['average_rating']?.toDouble() ?? 0.0,
      totalReviews: json['total_reviews'] ?? 0,
      pendingReplies: json['pending_replies'] ?? 0,
    );
  }
}
