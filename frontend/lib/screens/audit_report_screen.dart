import 'dart:typed_data';

import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';

import '../services/report_pdf_service.dart';
import '../widgets/app_snackbar.dart';
import '../widgets/glass_container.dart';

class AuditReportScreen extends StatelessWidget {
  final Map<String, dynamic> reportData;
  final String? reportTitle;

  const AuditReportScreen({super.key, required this.reportData, this.reportTitle});

  static const _bg = Color(0xFF0B1024);
  static const _darkText = Colors.white;
  static const _subtitleGrey = Color(0xFFC7D2FE);
  static const _primaryBlue = Color(0xFF3B82F6);

  Future<void> _downloadPdf(BuildContext context) async {
    final now = DateTime.now();
    final defaultName =
        '${(reportTitle ?? 'audit_report').replaceAll(' ', '_')}_${now.year}${now.month.toString().padLeft(2, '0')}${now.day.toString().padLeft(2, '0')}.pdf';

    try {
      final pdfBytes = await ReportPdfService.buildAuditPdf(
        reportTitle: reportTitle ?? 'Audit Report',
        reportData: reportData,
      );

      final savePath = await FilePicker.saveFile(
        dialogTitle: 'Save Audit Report PDF',
        fileName: defaultName,
        type: FileType.custom,
        allowedExtensions: ['pdf'],
        bytes: Uint8List.fromList(pdfBytes),
      );

      if (savePath == null || !context.mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        AppSnackbar.success('PDF downloaded to $savePath'),
      );
    } catch (e) {
      if (!context.mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        AppSnackbar.error('Failed to download PDF: $e'),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final auditAnalysis = reportData['audit_analysis'] as Map<String, dynamic>? ?? {};
    final processing = reportData['processing'] as Map<String, dynamic>? ?? {};
    final executiveSummary = reportData['executive_summary'] as String? ?? 'Audit complete.';

    final riskAssessment = auditAnalysis['risk_assessment'] as Map<String, dynamic>? ?? {};
    final violationAnalysis = auditAnalysis['violation_analysis'] as Map<String, dynamic>? ?? {};
    final visualization = auditAnalysis['visualization'] as Map<String, dynamic>? ?? {};
    final recommendations = auditAnalysis['recommendations'] as List? ?? [];
    final costTips = auditAnalysis['cost_optimization_tips'] as List? ?? [];
    final fraudSignals = auditAnalysis['fraud_signals'] as List? ?? [];
    final anomalies = auditAnalysis['anomalies'] as List? ?? [];

    return Scaffold(
      backgroundColor: _bg,
      extendBody: true,
      body: Stack(
        children: [
          Positioned(
            top: -100,
            left: -100,
            child: Container(
              width: 280,
              height: 280,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: const Color(0xFF5C6BC0).withValues(alpha: 0.18),
                boxShadow: [
                  BoxShadow(
                    color: const Color(0xFF5C6BC0).withValues(alpha: 0.2),
                    blurRadius: 100,
                  ),
                ],
              ),
            ),
          ),
          Positioned(
            bottom: -60,
            right: -60,
            child: Container(
              width: 240,
              height: 240,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: const Color(0xFF7C4DFF).withValues(alpha: 0.14),
                boxShadow: [
                  BoxShadow(
                    color: const Color(0xFF7C4DFF).withValues(alpha: 0.12),
                    blurRadius: 100,
                  ),
                ],
              ),
            ),
          ),
          SafeArea(
            bottom: false,
            child: CustomScrollView(
              slivers: [
                SliverAppBar(
                  backgroundColor: Colors.transparent,
                  elevation: 0,
                  scrolledUnderElevation: 0,
                  pinned: true,
                  centerTitle: true,
                  leading: IconButton(
                    icon: GlassContainer(
                      padding: const EdgeInsets.all(6),
                      borderRadius: BorderRadius.circular(10),
                      child: const Icon(Icons.arrow_back_ios_new_rounded, size: 16, color: _darkText),
                    ),
                    onPressed: () => Navigator.of(context).pop(),
                  ),
                  title: const Text(
                    'Audit Report',
                    style: TextStyle(color: _darkText, fontWeight: FontWeight.w700, fontSize: 18),
                  ),
                ),
                SliverPadding(
                  padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
                  sliver: SliverList(
                    delegate: SliverChildListDelegate([
                      _buildRiskBanner(riskAssessment),
                      const SizedBox(height: 20),
                      _buildExecutiveSummaryCard(executiveSummary),
                      const SizedBox(height: 24),
                      _buildStatsRow(violationAnalysis, processing),
                      const SizedBox(height: 24),
                      _buildTopSpendersChart(visualization),
                      const SizedBox(height: 24),
                      _buildCategoryDistribution(visualization),
                      const SizedBox(height: 24),
                      _buildViolationBreakdown(violationAnalysis),
                      const SizedBox(height: 24),
                      if (fraudSignals.isNotEmpty) ...[
                        _buildFraudSignals(fraudSignals),
                        const SizedBox(height: 24),
                      ],
                      if (anomalies.isNotEmpty) ...[
                        _buildAnomalies(anomalies),
                        const SizedBox(height: 24),
                      ],
                      if (recommendations.isNotEmpty) ...[
                        _buildRecommendations(recommendations),
                        const SizedBox(height: 24),
                      ],
                      if (costTips.isNotEmpty) ...[
                        _buildCostTips(costTips),
                        const SizedBox(height: 24),
                      ],
                      const SizedBox(height: 120),
                    ]),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
      bottomNavigationBar: SafeArea(
        top: false,
        child: Padding(
          padding: const EdgeInsets.fromLTRB(20, 0, 20, 16),
          child: GlassContainer(
            blur: 24,
            opacity: 0.10,
            borderRadius: BorderRadius.circular(20),
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
            border: Border.all(color: Colors.white.withValues(alpha: 0.12)),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                SizedBox(
                  width: double.infinity,
                  height: 54,
                  child: ElevatedButton.icon(
                    onPressed: () => _downloadPdf(context),
                    icon: const Icon(Icons.download_rounded, size: 22),
                    label: const Text(
                      'Download PDF Report',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700, letterSpacing: 0.3),
                    ),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: _primaryBlue,
                      foregroundColor: Colors.white,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                      elevation: 4,
                      shadowColor: _primaryBlue.withValues(alpha: 0.4),
                    ),
                  ),
                ),
                const SizedBox(height: 10),
                SizedBox(
                  width: double.infinity,
                  height: 50,
                  child: OutlinedButton.icon(
                    onPressed: () {},
                    icon: const Icon(Icons.edit_rounded, size: 20),
                    label: const Text(
                      'Edit Report Data',
                      style: TextStyle(fontSize: 15, fontWeight: FontWeight.w600),
                    ),
                    style: OutlinedButton.styleFrom(
                      foregroundColor: _primaryBlue,
                      side: const BorderSide(color: _primaryBlue, width: 1.5),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildRiskBanner(Map<String, dynamic> risk) {
    final level = (risk['overall_risk'] ?? 'unknown').toString().toUpperCase();
    final confidence = (risk['confidence_score'] ?? 0).toDouble();
    final keyRisks = risk['key_risks'] as List? ?? [];

    final riskColor = level == 'HIGH'
        ? const Color(0xFFF87171)
        : level == 'MEDIUM'
            ? const Color(0xFFFBBF24)
            : const Color(0xFF34D399);
    final riskIcon = level == 'HIGH'
        ? Icons.error_rounded
        : level == 'MEDIUM'
            ? Icons.warning_rounded
            : Icons.check_circle_rounded;

    return _sectionCard(
      title: 'Risk Overview',
      icon: riskIcon,
      iconColor: riskColor,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Text(
                '$level RISK',
                style: TextStyle(fontSize: 20, fontWeight: FontWeight.w800, color: riskColor, letterSpacing: 1),
              ),
              const Spacer(),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: Colors.white.withValues(alpha: 0.10),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  '${(confidence * 100).toInt()}% confidence',
                  style: TextStyle(fontSize: 11, fontWeight: FontWeight.w600, color: riskColor),
                ),
              ),
            ],
          ),
          if (keyRisks.isNotEmpty) ...[
            const SizedBox(height: 14),
            ...keyRisks.take(3).map(
              (r) => Padding(
                padding: const EdgeInsets.only(bottom: 6),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Icon(Icons.circle, size: 6, color: riskColor),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        r.toString(),
                        style: const TextStyle(fontSize: 13, color: _subtitleGrey, height: 1.3),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildExecutiveSummaryCard(String summary) {
    return _sectionCard(
      title: 'Executive Summary',
      icon: Icons.auto_awesome_rounded,
      iconColor: _primaryBlue,
      child: Text(
        summary,
        style: const TextStyle(fontSize: 14, color: _subtitleGrey, height: 1.6),
      ),
    );
  }

  Widget _buildStatsRow(Map<String, dynamic> violations, Map<String, dynamic> processing) {
    final total = violations['total_violations'] ?? 0;
    final critical = (violations['critical'] as List?)?.length ?? 0;
    final records = processing['total_records'] ?? 0;

    return Row(
      children: [
        _statChip('Records', records.toString(), const Color(0xFF60A5FA)),
        const SizedBox(width: 10),
        _statChip('Violations', total.toString(), const Color(0xFFFBBF24)),
        const SizedBox(width: 10),
        _statChip('Critical', critical.toString(), const Color(0xFFF87171)),
      ],
    );
  }

  Widget _statChip(String label, String value, Color color) {
    return Expanded(
      child: GlassContainer(
        blur: 18,
        opacity: 0.08,
        padding: const EdgeInsets.symmetric(vertical: 18),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.white.withValues(alpha: 0.10)),
        child: Column(
          children: [
            Text(
              value,
              style: TextStyle(fontSize: 28, fontWeight: FontWeight.w800, color: color),
            ),
            const SizedBox(height: 4),
            Text(
              label,
              style: const TextStyle(fontSize: 12, color: _subtitleGrey, fontWeight: FontWeight.w500),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildTopSpendersChart(Map<String, dynamic> viz) {
    final topSpenders = viz['top_spenders'] as List? ?? [];
    if (topSpenders.isEmpty) return const SizedBox.shrink();

    double maxAmount = 0;
    for (var s in topSpenders) {
      final a = (s['amount'] ?? 0).toDouble();
      if (a > maxAmount) maxAmount = a;
    }

    final colors = [
      const Color(0xFF60A5FA),
      const Color(0xFF8B5CF6),
      const Color(0xFFFBBF24),
      const Color(0xFF34D399),
      const Color(0xFFF472B6),
    ];

    return _sectionCard(
      title: 'Top Spenders',
      icon: Icons.people_rounded,
      iconColor: const Color(0xFF8B5CF6),
      child: Column(
        children: List.generate(topSpenders.length, (i) {
          final s = topSpenders[i];
          final name = s['employee'] ?? 'Unknown';
          final amount = (s['amount'] ?? 0).toDouble();
          final pct = maxAmount > 0 ? amount / maxAmount : 0.0;
          return Padding(
            padding: const EdgeInsets.only(bottom: 12),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Expanded(
                      child: Text(
                        name,
                        style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600, color: _darkText),
                      ),
                    ),
                    Text(
                      '\$${amount.toStringAsFixed(2)}',
                      style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: _subtitleGrey),
                    ),
                  ],
                ),
                const SizedBox(height: 6),
                ClipRRect(
                  borderRadius: BorderRadius.circular(8),
                  child: LinearProgressIndicator(
                    value: pct,
                    minHeight: 10,
                    backgroundColor: Colors.white.withValues(alpha: 0.08),
                    valueColor: AlwaysStoppedAnimation<Color>(colors[i % colors.length]),
                  ),
                ),
              ],
            ),
          );
        }),
      ),
    );
  }

  Widget _buildCategoryDistribution(Map<String, dynamic> viz) {
    final categories = viz['category_distribution'] as List? ?? [];
    if (categories.isEmpty) return const SizedBox.shrink();

    double total = 0;
    for (var c in categories) {
      total += (c['value'] ?? 0).toDouble();
    }

    return _sectionCard(
      title: 'Category Distribution',
      icon: Icons.pie_chart_rounded,
      iconColor: const Color(0xFF10B981),
      child: Column(
        children: categories.map((c) {
          final name = c['category'] ?? 'Unknown';
          final value = (c['value'] ?? 0).toDouble();
          final pct = total > 0 ? value / total : 0.0;
          return Padding(
            padding: const EdgeInsets.only(bottom: 12),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Expanded(
                      child: Text(
                        name,
                        style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600, color: _darkText),
                      ),
                    ),
                    Text(
                      '${(pct * 100).toStringAsFixed(0)}%',
                      style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: _subtitleGrey),
                    ),
                  ],
                ),
                const SizedBox(height: 6),
                LinearProgressIndicator(
                  value: pct,
                  minHeight: 10,
                  backgroundColor: Colors.white.withValues(alpha: 0.08),
                  valueColor: const AlwaysStoppedAnimation<Color>(Color(0xFF10B981)),
                ),
              ],
            ),
          );
        }).toList(),
      ),
    );
  }

  Widget _buildViolationBreakdown(Map<String, dynamic> violations) {
    final critical = violations['critical'] as List? ?? [];
    final moderate = violations['moderate'] as List? ?? [];
    final minor = violations['minor'] as List? ?? [];

    if (critical.isEmpty && moderate.isEmpty && minor.isEmpty) {
      return _sectionCard(
        title: 'Violations',
        icon: Icons.shield_rounded,
        iconColor: const Color(0xFF34D399),
        child: const Row(
          children: [
            Icon(Icons.check_circle_rounded, color: Color(0xFF34D399), size: 20),
            SizedBox(width: 10),
            Text(
              'No violations detected!',
              style: TextStyle(color: Color(0xFF34D399), fontWeight: FontWeight.w600),
            ),
          ],
        ),
      );
    }

    return _sectionCard(
      title: 'Policy Violations',
      icon: Icons.gavel_rounded,
      iconColor: const Color(0xFFF87171),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (critical.isNotEmpty) ...[
            _violationHeader('Critical', critical.length, const Color(0xFFF87171)),
            ...critical.map((v) => _violationItem(v, const Color(0xFFF87171))),
            const SizedBox(height: 12),
          ],
          if (moderate.isNotEmpty) ...[
            _violationHeader('Moderate', moderate.length, const Color(0xFFFBBF24)),
            ...moderate.map((v) => _violationItem(v, const Color(0xFFFBBF24))),
            const SizedBox(height: 12),
          ],
          if (minor.isNotEmpty) ...[
            _violationHeader('Minor', minor.length, const Color(0xFF94A3B8)),
            ...minor.map((v) => _violationItem(v, const Color(0xFF94A3B8))),
          ],
        ],
      ),
    );
  }

  Widget _violationHeader(String severity, int count, Color color) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
        decoration: BoxDecoration(
          color: color.withValues(alpha: 0.12),
          borderRadius: BorderRadius.circular(6),
        ),
        child: Text(
          '$severity ($count)',
          style: TextStyle(fontSize: 12, fontWeight: FontWeight.w700, color: color),
        ),
      ),
    );
  }

  Widget _violationItem(dynamic v, Color color) {
    return Container(
      margin: const EdgeInsets.only(bottom: 8),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.08),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color.withValues(alpha: 0.18)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Expanded(
                child: Text(
                  v['employee'] ?? '',
                  style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14, color: _darkText),
                ),
              ),
              Text(
                '\$${(v['amount'] ?? 0).toStringAsFixed(2)}',
                style: TextStyle(fontWeight: FontWeight.w700, fontSize: 14, color: color),
              ),
            ],
          ),
          const SizedBox(height: 4),
          Text(
            v['description'] ?? '',
            style: const TextStyle(fontSize: 12, color: _subtitleGrey, height: 1.3),
          ),
        ],
      ),
    );
  }

  Widget _buildFraudSignals(List signals) {
    return _sectionCard(
      title: 'Fraud Signals',
      icon: Icons.local_fire_department_rounded,
      iconColor: const Color(0xFFF87171),
      child: Column(
        children: signals.map((s) {
          final severity = (s['severity'] ?? 'medium').toString();
          final color = severity == 'critical' ? const Color(0xFFF87171) : const Color(0xFFFBBF24);
          return Container(
            margin: const EdgeInsets.only(bottom: 8),
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: color.withValues(alpha: 0.10),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: color.withValues(alpha: 0.18)),
            ),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Icon(Icons.warning_rounded, size: 18, color: color),
                const SizedBox(width: 10),
                Expanded(
                  child: Text(
                    s['description'] ?? '',
                    style: const TextStyle(fontSize: 13, color: _darkText, height: 1.45),
                  ),
                ),
              ],
            ),
          );
        }).toList(),
      ),
    );
  }

  Widget _buildAnomalies(List anomalies) {
    return _sectionCard(
      title: 'Anomalies Detected',
      icon: Icons.troubleshoot_rounded,
      iconColor: const Color(0xFF8B5CF6),
      child: Column(
        children: anomalies.map((a) {
          return Container(
            margin: const EdgeInsets.only(bottom: 8),
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: const Color(0xFF8B5CF6).withValues(alpha: 0.10),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: const Color(0xFF8B5CF6).withValues(alpha: 0.18)),
            ),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Icon(Icons.insights_rounded, size: 18, color: Color(0xFFC4B5FD)),
                const SizedBox(width: 10),
                Expanded(
                  child: Text(
                    a['description'] ?? '',
                    style: const TextStyle(fontSize: 13, color: _darkText, height: 1.45),
                  ),
                ),
              ],
            ),
          );
        }).toList(),
      ),
    );
  }

  Widget _buildRecommendations(List recs) {
    return _sectionCard(
      title: 'Recommendations',
      icon: Icons.lightbulb_rounded,
      iconColor: _primaryBlue,
      child: Column(
        children: recs.map((r) {
          final priority = (r['priority'] ?? 'medium').toString();
          final pColor = priority == 'high'
              ? const Color(0xFFF87171)
              : priority == 'medium'
                  ? const Color(0xFFFBBF24)
                  : const Color(0xFF34D399);

          return Container(
            margin: const EdgeInsets.only(bottom: 10),
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              color: Colors.white.withValues(alpha: 0.06),
              borderRadius: BorderRadius.circular(14),
              border: Border.all(color: Colors.white.withValues(alpha: 0.10)),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                      decoration: BoxDecoration(
                        color: pColor.withValues(alpha: 0.18),
                        borderRadius: BorderRadius.circular(6),
                        border: Border.all(color: pColor.withValues(alpha: 0.25)),
                      ),
                      child: Text(
                        priority.toUpperCase(),
                        style: TextStyle(fontSize: 10, fontWeight: FontWeight.w800, color: pColor),
                      ),
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        r['title'] ?? '',
                        style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 14, color: _darkText),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 6),
                Text(
                  r['description'] ?? '',
                  style: const TextStyle(fontSize: 13, color: _subtitleGrey, height: 1.45),
                ),
              ],
            ),
          );
        }).toList(),
      ),
    );
  }

  Widget _buildCostTips(List tips) {
    return _sectionCard(
      title: 'Cost Optimization',
      icon: Icons.savings_rounded,
      iconColor: const Color(0xFF10B981),
      child: Column(
        children: tips.map((t) {
          return Container(
            margin: const EdgeInsets.only(bottom: 10),
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [
                  const Color(0xFF10B981).withValues(alpha: 0.14),
                  const Color(0xFF10B981).withValues(alpha: 0.06),
                ],
              ),
              borderRadius: BorderRadius.circular(14),
              border: Border.all(color: const Color(0xFF10B981).withValues(alpha: 0.22)),
            ),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  padding: const EdgeInsets.all(6),
                  decoration: BoxDecoration(
                    color: Colors.white.withValues(alpha: 0.10),
                    shape: BoxShape.circle,
                    border: Border.all(color: Colors.white.withValues(alpha: 0.20)),
                  ),
                  child: const Icon(Icons.lightbulb_outline, color: Color(0xFFE6FFF5), size: 16),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        t['tip'] ?? '',
                        style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 14, color: _darkText),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        t['description'] ?? '',
                        style: const TextStyle(fontSize: 12, color: Color(0xFFCFF7E8), height: 1.45),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          );
        }).toList(),
      ),
    );
  }

  Widget _sectionCard({
    required String title,
    required IconData icon,
    required Color iconColor,
    required Widget child,
  }) {
    return GlassContainer(
      blur: 22,
      opacity: 0.08,
      padding: const EdgeInsets.all(20),
      borderRadius: BorderRadius.circular(20),
      border: Border.all(color: Colors.white.withValues(alpha: 0.12)),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: iconColor.withValues(alpha: 0.14),
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Icon(icon, color: iconColor, size: 18),
              ),
              const SizedBox(width: 12),
              Text(
                title,
                style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w700, color: _darkText),
              ),
            ],
          ),
          const SizedBox(height: 18),
          child,
        ],
      ),
    );
  }
}
