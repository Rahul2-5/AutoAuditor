import 'package:flutter/material.dart';

import '../widgets/report_list_tile.dart';
import '../widgets/glass_container.dart';

class ReportsScreen extends StatelessWidget {
  final List<Map<String, dynamic>> reports;
  final ValueChanged<Map<String, dynamic>> onOpenReport;

  const ReportsScreen({
    super.key,
    required this.reports,
    required this.onOpenReport,
  });

  static const _lightText = Colors.white;
  static const _subtitleGrey = Color(0xFF94A3B8);

  String _formatDate(DateTime date) {
    const months = [
      'Jan',
      'Feb',
      'Mar',
      'Apr',
      'May',
      'Jun',
      'Jul',
      'Aug',
      'Sep',
      'Oct',
      'Nov',
      'Dec',
    ];
    return '${months[date.month - 1]} ${date.day}, ${date.year}';
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'All Reports',
            style: TextStyle(
              fontSize: 26,
              fontWeight: FontWeight.w800,
              color: _lightText,
            ),
          ),
          const SizedBox(height: 6),
          Text(
            'Select any audit report to view full details',
            style: TextStyle(
              color: _subtitleGrey,
              fontSize: 14,
            ),
          ),
          const SizedBox(height: 20),
          if (reports.isEmpty)
            _buildEmptyState()
          else
            ...reports.map((report) {
              final status = (report['status'] ?? 'Completed').toString();
              final statusColor =
                  status == 'Flagged' ? const Color(0xFFEF4444) : const Color(0xFF10B981);

              final date = report['date'] is DateTime ? report['date'] as DateTime : DateTime.now();
              final items = (report['items'] ?? 0).toString();

              return GestureDetector(
                onTap: () => onOpenReport(report),
                child: ReportListTile(
                  title: (report['title'] ?? 'Untitled Audit').toString(),
                  subtitle: '${_formatDate(date)} • $items items',
                  status: status,
                  statusColor: statusColor,
                  statusBgColor: statusColor.withValues(alpha: 0.1),
                ),
              );
            }),
          const SizedBox(height: 24),
        ],
      ),
    );
  }

  Widget _buildEmptyState() {
    return GlassContainer(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(vertical: 42, horizontal: 24),
      borderRadius: BorderRadius.circular(18),
      child: const Column(
        children: [
          Icon(Icons.receipt_long_rounded, size: 48, color: Color(0xFF9CA3AF)),
          SizedBox(height: 12),
          Text(
            'No reports available',
            style: TextStyle(
              fontSize: 17,
              fontWeight: FontWeight.w700,
              color: _lightText,
            ),
          ),
          SizedBox(height: 4),
          Text(
            'Run an audit to see reports listed here.',
            style: TextStyle(fontSize: 13, color: _subtitleGrey),
          ),
        ],
      ),
    );
  }
}
