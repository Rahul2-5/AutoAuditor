import 'package:pdf/pdf.dart';
import 'package:pdf/widgets.dart' as pw;

class ReportPdfService {
  static Future<List<int>> buildAuditPdf({
    required String reportTitle,
    required Map<String, dynamic> reportData,
  }) async {
    final pdf = pw.Document();

    final auditAnalysis = reportData['audit_analysis'] as Map<String, dynamic>? ?? {};
    final processing = reportData['processing'] as Map<String, dynamic>? ?? {};
    final riskAssessment = auditAnalysis['risk_assessment'] as Map<String, dynamic>? ?? {};
    final violationAnalysis = auditAnalysis['violation_analysis'] as Map<String, dynamic>? ?? {};

    final executiveSummary =
        (reportData['executive_summary'] ?? 'Audit completed successfully.').toString();

    final overallRisk = (riskAssessment['overall_risk'] ?? 'unknown').toString().toUpperCase();
    final confidenceScore = _toDouble(riskAssessment['confidence_score']) * 100;
    final records = _toInt(processing['total_records']);
    final totalViolations = _toInt(violationAnalysis['total_violations']);

    final critical = (violationAnalysis['critical'] as List?) ?? const [];
    final moderate = (violationAnalysis['moderate'] as List?) ?? const [];
    final minor = (violationAnalysis['minor'] as List?) ?? const [];

    final allViolations = [
      ...critical,
      ...moderate,
      ...minor,
    ];

    pdf.addPage(
      pw.MultiPage(
        pageTheme: pw.PageTheme(
          margin: const pw.EdgeInsets.all(30),
          theme: pw.ThemeData.withFont(
            base: pw.Font.helvetica(),
            bold: pw.Font.helveticaBold(),
          ),
        ),
        build: (context) => [
          pw.Container(
            padding: const pw.EdgeInsets.only(bottom: 12),
            decoration: const pw.BoxDecoration(
              border: pw.Border(bottom: pw.BorderSide(color: PdfColors.grey300, width: 1)),
            ),
            child: pw.Row(
              mainAxisAlignment: pw.MainAxisAlignment.spaceBetween,
              crossAxisAlignment: pw.CrossAxisAlignment.start,
              children: [
                pw.Column(
                  crossAxisAlignment: pw.CrossAxisAlignment.start,
                  children: [
                    pw.Text(
                      'AuditCore AI',
                      style: pw.TextStyle(
                        font: pw.Font.helveticaBold(),
                        color: PdfColor.fromHex('#1D4ED8'),
                        fontSize: 22,
                      ),
                    ),
                    pw.SizedBox(height: 4),
                    pw.Text(
                      'AUTOMATED COMPLIANCE REPORT',
                      style: const pw.TextStyle(
                        fontSize: 10,
                        color: PdfColors.grey700,
                        letterSpacing: 1,
                      ),
                    ),
                  ],
                ),
                pw.Column(
                  crossAxisAlignment: pw.CrossAxisAlignment.end,
                  children: [
                    pw.Text(
                      reportTitle,
                      style: pw.TextStyle(font: pw.Font.helveticaBold(), fontSize: 14),
                    ),
                    pw.SizedBox(height: 4),
                    pw.Text(
                      'Generated: ${DateTime.now().toIso8601String().split('T').first}',
                      style: const pw.TextStyle(fontSize: 10, color: PdfColors.grey700),
                    ),
                  ],
                ),
              ],
            ),
          ),
          pw.SizedBox(height: 18),
          pw.Text(
            'Executive Summary',
            style: pw.TextStyle(font: pw.Font.helveticaBold(), fontSize: 18),
          ),
          pw.SizedBox(height: 12),
          pw.Row(
            children: [
              _metricCard('TOTAL RECORDS', '$records', PdfColor.fromHex('#111827')),
              pw.SizedBox(width: 10),
              _metricCard('FLAGGED VIOLATIONS', '$totalViolations', PdfColor.fromHex('#DC2626')),
              pw.SizedBox(width: 10),
              _metricCard('AI CONFIDENCE SCORE', '${confidenceScore.toStringAsFixed(1)}%', PdfColor.fromHex('#2563EB')),
            ],
          ),
          pw.SizedBox(height: 16),
          pw.Container(
            padding: const pw.EdgeInsets.all(12),
            decoration: pw.BoxDecoration(
              color: PdfColor.fromHex('#F8FAFC'),
              borderRadius: pw.BorderRadius.circular(8),
            ),
            child: pw.Column(
              crossAxisAlignment: pw.CrossAxisAlignment.start,
              children: [
                pw.Text(
                  'Overall Risk: $overallRisk',
                  style: pw.TextStyle(
                    font: pw.Font.helveticaBold(),
                    fontSize: 12,
                    color: overallRisk == 'HIGH'
                        ? PdfColor.fromHex('#DC2626')
                        : overallRisk == 'MEDIUM'
                            ? PdfColor.fromHex('#D97706')
                            : PdfColor.fromHex('#059669'),
                  ),
                ),
                pw.SizedBox(height: 6),
                pw.Text(
                  executiveSummary,
                  style: const pw.TextStyle(fontSize: 11, color: PdfColors.grey800, lineSpacing: 2),
                ),
              ],
            ),
          ),
          pw.SizedBox(height: 18),
          pw.Text(
            'Flagged Violations Detail',
            style: pw.TextStyle(font: pw.Font.helveticaBold(), fontSize: 16),
          ),
          pw.SizedBox(height: 10),
          if (allViolations.isEmpty)
            pw.Container(
              width: double.infinity,
              padding: const pw.EdgeInsets.all(12),
              decoration: pw.BoxDecoration(
                border: pw.Border.all(color: PdfColors.grey300),
                borderRadius: pw.BorderRadius.circular(8),
              ),
              child: pw.Text('No violations detected.'),
            )
          else
            pw.Table(
              border: pw.TableBorder.all(color: PdfColors.grey300, width: 0.6),
              columnWidths: {
                0: const pw.FlexColumnWidth(1.2),
                1: const pw.FlexColumnWidth(1.6),
                2: const pw.FlexColumnWidth(1.1),
                3: const pw.FlexColumnWidth(2.4),
              },
              children: [
                pw.TableRow(
                  decoration: pw.BoxDecoration(color: PdfColor.fromHex('#EFF6FF')),
                  children: [
                    _tableHeader('DATE'),
                    _tableHeader('EMPLOYEE'),
                    _tableHeader('AMOUNT'),
                    _tableHeader('VIOLATION'),
                  ],
                ),
                ...allViolations.take(20).map((item) {
                  return pw.TableRow(
                    children: [
                      _tableCell((item['date'] ?? '-').toString()),
                      _tableCell((item['employee'] ?? '-').toString()),
                      _tableCell('\$${_toDouble(item['amount']).toStringAsFixed(2)}'),
                      _tableCell((item['description'] ?? item['violation_type'] ?? '-').toString()),
                    ],
                  );
                }),
              ],
            ),
          pw.SizedBox(height: 24),
          pw.Container(
            padding: const pw.EdgeInsets.all(12),
            decoration: pw.BoxDecoration(
              border: pw.Border.all(color: PdfColors.grey300),
              borderRadius: pw.BorderRadius.circular(8),
            ),
            child: pw.Column(
              crossAxisAlignment: pw.CrossAxisAlignment.start,
              children: [
                pw.Text(
                  'AI Audit Conclusion',
                  style: pw.TextStyle(font: pw.Font.helveticaBold(), fontSize: 13),
                ),
                pw.SizedBox(height: 6),
                pw.Text(
                  executiveSummary,
                  style: const pw.TextStyle(fontSize: 11, color: PdfColors.grey800, lineSpacing: 2),
                ),
              ],
            ),
          ),
        ],
      ),
    );

    return pdf.save();
  }

  static pw.Widget _metricCard(String label, String value, PdfColor valueColor) {
    return pw.Expanded(
      child: pw.Container(
        padding: const pw.EdgeInsets.all(10),
        decoration: pw.BoxDecoration(
          border: pw.Border.all(color: PdfColors.grey300),
          borderRadius: pw.BorderRadius.circular(6),
        ),
        child: pw.Column(
          crossAxisAlignment: pw.CrossAxisAlignment.start,
          children: [
            pw.Text(
              label,
              style: const pw.TextStyle(fontSize: 8, color: PdfColors.grey700),
            ),
            pw.SizedBox(height: 8),
            pw.Text(
              value,
              style: pw.TextStyle(
                font: pw.Font.helveticaBold(),
                fontSize: 22,
                color: valueColor,
              ),
            ),
          ],
        ),
      ),
    );
  }

  static pw.Widget _tableHeader(String text) {
    return pw.Padding(
      padding: const pw.EdgeInsets.all(6),
      child: pw.Text(
        text,
        style: pw.TextStyle(font: pw.Font.helveticaBold(), fontSize: 9),
      ),
    );
  }

  static pw.Widget _tableCell(String text) {
    return pw.Padding(
      padding: const pw.EdgeInsets.all(6),
      child: pw.Text(
        text,
        style: const pw.TextStyle(fontSize: 9),
      ),
    );
  }

  static int _toInt(dynamic value) {
    if (value is int) return value;
    if (value is num) return value.toInt();
    return int.tryParse(value?.toString() ?? '') ?? 0;
  }

  static double _toDouble(dynamic value) {
    if (value is double) return value;
    if (value is num) return value.toDouble();
    return double.tryParse(value?.toString() ?? '') ?? 0;
  }
}
