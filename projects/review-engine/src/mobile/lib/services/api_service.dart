import dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../models/models.dart';

class ApiService {
  // Use String.fromEnvironment for easy configuration
  static const String baseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://10.0.2.2:8000', // Android emulator localhost
  );
  
  final _storage = const FlutterSecureStorage();

  Future<String?> getToken() async {
    return await _storage.read(key: 'access_token');
  }

  Future<bool> login(String email, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/token'),
      body: {
        'username': email,
        'password': password,
      },
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      await _storage.write(key: 'access_token', value: data['access_token']);
      // In a real app, we'd store business_id if the login response provided it.
      // For now, we rely on the backend to infer business context from the JWT.
      return true;
    }
    return false;
  }

  Future<void> logout() async {
    await _storage.delete(key: 'access_token');
  }

  Future<DashboardStats?> getStats() async {
    final token = await getToken();
    final response = await http.get(
      Uri.parse('$baseUrl/reviews/stats'),
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      return DashboardStats.fromJson(json.decode(response.body));
    }
    return null;
  }

  Future<List<Review>> getReviews() async {
    final token = await getToken();
    final response = await http.get(
      Uri.parse('$baseUrl/google/reviews'),
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      final List data = json.decode(response.body);
      return data.map((item) => Review.fromJson(item)).toList();
    }
    return [];
  }

  Future<String?> generateAiReply(String reviewText) async {
    final token = await getToken();
    final response = await http.post(
      Uri.parse('$baseUrl/reviews/generate-reply'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: json.encode({
        'review_text': reviewText,
        'star_rating': 5 // Default high rating for generated reply context
      }),
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['reply'];
    }
    return null;
  }

  Future<bool> postReply(String reviewId, String reply) async {
    final token = await getToken();
    final response = await http.post(
      Uri.parse('$baseUrl/google/reviews/reply'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: json.encode({
        'review_id': reviewId,
        'reply': reply,
      }),
    );

    return response.statusCode == 200;
  }

  Future<bool> sendReviewRequest(String name, String contact) async {
    final token = await getToken();
    final response = await http.post(
      Uri.parse('$baseUrl/reviews/request'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: json.encode({
        'customer_name': name,
        'contact': contact,
        // Backend now handles business_id lookup via user session
      }),
    );

    return response.statusCode == 200;
  }
}
