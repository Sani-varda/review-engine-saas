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
      reviewerName: json['reviewer']?['displayName'] ?? 'Anonymous',
      comment: json['comment'] ?? '',
      starRating: _parseStarRating(json['starRating']),
      createTime: DateTime.parse(json['createTime'] ?? DateTime.now().toIsoformat()),
      reply: json['reviewReply']?['comment'],
    );
  }

  static int _parseStarRating(dynamic rating) {
    if (rating == 'FIVE') return 5;
    if (rating == 'FOUR') return 4;
    if (rating == 'THREE') return 3;
    if (rating == 'TWO') return 2;
    if (rating == 'ONE') return 1;
    if (rating is int) return rating;
    return 0;
  }
}

class DashboardStats {
  final double averageRating;
  final int totalRequests;
  final int completedReviews;
  final double conversionRate;

  DashboardStats({
    required this.averageRating,
    required this.totalRequests,
    required this.completedReviews,
    required this.conversionRate,
  });

  factory DashboardStats.fromJson(Map<String, dynamic> json) {
    return DashboardStats(
      averageRating: json['avg_rating']?.toDouble() ?? 0.0,
      totalRequests: json['total'] ?? 0,
      completedReviews: json['completed'] ?? 0,
      conversionRate: json['conversion_rate']?.toDouble() ?? 0.0,
    );
  }
}
