import 'dart:io';
import 'lib/services/ollama_service.dart';

void main() async {
  print('Reading test_expenses.csv...');
  final file = File('test_expenses.csv');
  if (!await file.exists()) {
    print('File not found!');
    return;
  }
  
  final text = await file.readAsString();
  print('Extracted \\n---start---\\n\$text\\n---end---');
  print('Connecting to Ollama...');
  
  final service = OllamaService();
  final response = await service.analyzeExpenses(text);
  
  print('\\n--- OLLAMA RESPONSE ---');
  print(response);
}