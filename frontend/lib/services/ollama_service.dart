import 'dart:convert';
import 'dart:io' show Platform;
import 'package:http/http.dart' as http;

class OllamaService {
  static String get _baseUrl {
    if (Platform.isAndroid) {
      // 10.0.2.2 is the special IP alias to the host loopback interface in Android emulators
      return 'http://10.0.2.2:11434/api/generate';
    } else {
      return 'http://127.0.0.1:11434/api/generate';
    }
  }
  static const String _model = 'llama3:8b-instruct-q4_0';

  Future<Map<String, dynamic>?> analyzeExpenses(String expenseData) async {
    const prompt = '''
You are an expert AI Corporate Expense Auditor. Carefully analyze the text below which contains expense report data (e.g. from a CSV).

Identify:
1. Anomalies or suspicious transactions (e.g., unusually high amounts, late night purchases, prohibited items, duplicates).
2. Out-of-policy warnings.
3. An estimate of potential savings if these items were rejected.

IMPORTANT: You MUST respond ONLY with a valid JSON object matching this exact structure, with no additional text or markdown formatting outside the JSON:
{
  "anomalies_count": 0,
  "estimated_savings": 0.0,
  "summary": "string describing the findings",
  "flagged_items": [
    {
      "date": "YYYY-MM-DD",
      "description": "item description",
      "reason": "why it was flagged"
    }
  ]
}

EXPENSE DATA:
''';

    try {
      final response = await http.post(
        Uri.parse(_baseUrl),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'model': _model,
          'prompt': prompt + expenseData,
          'stream': false,
          'format': 'json',
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        String rawResponse = data['response'] ?? '{}';

        // Clean up formatting block if Llama adds it
        rawResponse = rawResponse
            .replaceAll('```json', '')
            .replaceAll('```', '')
            .trim();
            
        // Try to robustly extract only the JSON payload in case LLM adds chat text
        final startIndex = rawResponse.indexOf('{');
        final endIndex = rawResponse.lastIndexOf('}');
        if (startIndex != -1 && endIndex != -1 && endIndex >= startIndex) {
          rawResponse = rawResponse.substring(startIndex, endIndex + 1);
        }

        try {
          return jsonDecode(rawResponse) as Map<String, dynamic>;
        } catch (e) {
          print('Failed to parse JSON exactly: \$rawResponse');
          return null; // Handle parse failure
        }
      }
    } catch (e) {
      print('Error connecting to Ollama: \$e');
    }
    return null;
  }
}
