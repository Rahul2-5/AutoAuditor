import 'dart:convert';
import 'dart:io' show File, Platform;
import 'package:http/http.dart' as http;

class BackendService {
  // Update this to match your actual backend URL (e.g. FastAPI, Flask, Node.js)
  static String get _baseUrl {
    if (Platform.isAndroid) {
      // 10.0.2.2 is the special IP alias to the host loopback interface in Android emulators
      // Port 8000 is common for FastAPI/Django/Flask. Change to your backends port.
      return 'http://10.0.2.2:8000';
    } else {
      return 'http://127.0.0.1:8000';
    }
  }

  /// Sends the CSV file to the backend for auditing.
  /// Ensure your backend has a corresponding POST endpoint (e.g. `/api/full-audit`)
  Future<Map<String, dynamic>?> analyzeExpenses(String fileContent) async {
    final endpoint = Uri.parse('$_baseUrl/api/full-audit');

    try {
      // Create a multipart request for the CSV file
      var request = http.MultipartRequest('POST', endpoint);
      
      // Attach the CSV content as a file
      request.files.add(
        http.MultipartFile.fromString(
          'file', // Ensure this matches your backend's expected field name (e.g. 'file' in FastAPI/Flask)
          fileContent,
          filename: 'expenses.csv',
        ),
      );

      print('Sending file to backend: \$endpoint');
      final streamedResponse = await request.send();
      final response = await http.Response.fromStream(streamedResponse);

      print('Backend Response Status: \${response.statusCode}');

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data as Map<String, dynamic>;
      } else {
        print('Backend Error: \${response.body}');
      }
    } catch (e) {
      print('Error connecting to backend: \$e');
    }
    return null;
  }

  /// Sends a PDF file to the backend for auditing.
  Future<Map<String, dynamic>?> analyzeExpensesPdf(File pdfFile) async {
    final endpoint = Uri.parse('$_baseUrl/api/full-audit');

    try {
      var request = http.MultipartRequest('POST', endpoint);

      request.files.add(
        await http.MultipartFile.fromPath(
          'file',
          pdfFile.path,
          filename: pdfFile.path.split(RegExp(r'[/\\]')).last,
        ),
      );

      print('Sending PDF to backend: \$endpoint');
      final streamedResponse = await request.send();
      final response = await http.Response.fromStream(streamedResponse);

      print('Backend Response Status: \${response.statusCode}');

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data as Map<String, dynamic>;
      } else {
        print('Backend Error: \${response.body}');
      }
    } catch (e) {
      print('Error connecting to backend: \$e');
    }
    return null;
  }
}
