import 'dart:io';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';

import '../services/backend_service.dart';
import 'audit_loading_screen.dart';
import 'audit_report_screen.dart';
import 'reports_screen.dart';
import '../widgets/app_snackbar.dart';
import '../widgets/glass_container.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  int _currentNavIndex = 0;
  final BackendService _backendService = BackendService();

  // Store recent reports
  List<Map<String, dynamic>> _recentReports = [];

  // Color palette
  static const _primaryBlue = Color(0xFF3B82F6);
  static const _darkBg = Color(0xFF0F172A);
  static const _lightText = Colors.white;
  static const _subtitleGrey = Color(0xFF94A3B8);

  Future<void> _pickAndAnalyze() async {
    final result = await FilePicker.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['csv', 'pdf'],
    );

    if (result != null && result.files.single.path != null) {
      final pickedPath = result.files.single.path!;
      final fileName = result.files.single.name;
      final extension = pickedPath.toLowerCase().split('.').last;

      if (extension != 'csv' && extension != 'pdf') {
        if (!mounted) return;
        ScaffoldMessenger.of(context).showSnackBar(
          AppSnackbar.error('Only CSV and PDF files are supported.'),
        );
        return;
      }

      // Show snackbar when user uploads a file for audit
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        AppSnackbar.success('Uploading $fileName for audit...'),
      );

      final file = File(pickedPath);
      if (!mounted) return;

      // Create the backend future based on file type
      late Future<Map<String, dynamic>?> analysisFuture;
      if (extension == 'csv') {
        final fileText = await file.readAsString();
        analysisFuture = _backendService.analyzeExpenses(fileText);
      } else {
        // PDF: send as binary upload
        analysisFuture = _backendService.analyzeExpensesPdf(file);
      }

      // Navigate to the animated loading screen, passing the backend future
      final returnedResult = await Navigator.of(context).push<Map<String, dynamic>?>(
        PageRouteBuilder(
          pageBuilder: (_, __, ___) => AuditLoadingScreen(
            analysisFuture: analysisFuture,
            fileName: fileName,
          ),
          transitionsBuilder: (_, animation, __, child) {
            return FadeTransition(
              opacity: animation,
              child: SlideTransition(
                position: Tween<Offset>(
                  begin: const Offset(0, 0.05),
                  end: Offset.zero,
                ).animate(CurvedAnimation(parent: animation, curve: Curves.easeOut)),
                child: child,
              ),
            );
          },
          transitionDuration: const Duration(milliseconds: 400),
        ),
      );

      // If loading screen returned an error result (backend failed), show snackbar
      if (returnedResult != null && returnedResult['status'] != 'success') {
        if (!mounted) return;
        final errorMessage = returnedResult['message'] ?? 'Error analyzing file';
        ScaffoldMessenger.of(context).showSnackBar(
          AppSnackbar.error(errorMessage),
        );
      } else if (returnedResult != null && returnedResult['status'] == 'success') {
        // Add the completed audit to recent reports
        if (!mounted) return;
        final report = returnedResult['report'] ?? {};
        _addToRecentReports(fileName, report);
      }
    }
  }

  void _addToRecentReports(String fileName, Map<String, dynamic> reportData) {
    final processing = reportData['processing'] as Map<String, dynamic>? ?? {};
    final auditAnalysis = reportData['audit_analysis'] as Map<String, dynamic>? ?? {};
    final violationAnalysis = auditAnalysis['violation_analysis'] as Map<String, dynamic>? ?? {};

    final totalItems =
        processing['total_records'] ??
        processing['rows_processed'] ??
        processing['total_rows'] ??
        reportData['transaction_count'] ??
        0;

    final violationCount =
        violationAnalysis['total_violations'] ??
        reportData['flagged_count'] ??
        0;

    final newReport = {
      'title': fileName.replaceAll('.csv', '').replaceAll('.pdf', ''),
      'date': DateTime.now(),
      'items': totalItems is int ? totalItems : int.tryParse(totalItems.toString()) ?? 0,
      'status': (violationCount is int ? violationCount : int.tryParse(violationCount.toString()) ?? 0) > 0
          ? 'Flagged'
          : 'Completed',
      'fullReport': reportData,
    };

    setState(() {
      _recentReports.insert(0, newReport);
    });

    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      AppSnackbar.success('✓ Audit completed! Added to Recent Reports.'),
    );
  }

  String _formatDate(DateTime date) {
    final months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return '${months[date.month - 1]} ${date.day}, ${date.year}';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: _darkBg,
      extendBody: true,
      body: Stack(
        children: [
          // Background Glows
          Positioned(
            top: -100,
            left: -100,
            child: Container(
              width: 300,
              height: 300,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: const Color(0xFF6366F1).withValues(alpha: 0.15),
                boxShadow: [
                  BoxShadow(color: const Color(0xFF6366F1).withValues(alpha: 0.2), blurRadius: 100)
                ],
              ),
            ),
          ),
          Positioned(
            bottom: -50,
            right: -50,
            child: Container(
              width: 250,
              height: 250,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: const Color(0xFF3B82F6).withValues(alpha: 0.15),
                boxShadow: [
                  BoxShadow(color: const Color(0xFF3B82F6).withValues(alpha: 0.2), blurRadius: 100)
                ],
              ),
            ),
          ),
          SafeArea(
            bottom: false,
            child: _currentNavIndex == 2
                ? ReportsScreen(
                    reports: _recentReports,
                    onOpenReport: (report) {
                      if (report['fullReport'] != null) {
                        Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (_) => AuditReportScreen(
                              reportData: report['fullReport'],
                              reportTitle: (report['title'] ?? 'Audit Report').toString(),
                            ),
                          ),
                        );
                      }
                    },
                  )
                : SingleChildScrollView(
                    padding: const EdgeInsets.only(left: 20, right: 20, bottom: 120),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const SizedBox(height: 8),
                        _buildAppBar(),
                        const SizedBox(height: 28),
                        _buildGreeting(),
                        const SizedBox(height: 28),
                        _buildUploadCard(),
                        const SizedBox(height: 18),
                        _buildAnalyzeButton(),
                        const SizedBox(height: 32),
                        _buildRecentReportsSection(),
                        const SizedBox(height: 24),
                      ],
                    ),
                  ),
          ),
        ],
      ),
      bottomNavigationBar: _buildBottomNav(),
    );
  }

  void _openReportFromDashboard(Map<String, dynamic> report) {
    if (report['fullReport'] != null) {
      Navigator.of(context).push(
        MaterialPageRoute(
          builder: (_) => AuditReportScreen(
            reportData: report['fullReport'],
            reportTitle: (report['title'] ?? 'Audit Report').toString(),
          ),
        ),
      );
    }
  }

  // ── App Bar ──────────────────────────────────────────────────────────────────

  Widget _buildAppBar() {
    return Row(
      children: [
        GlassContainer(
          padding: const EdgeInsets.all(8),
          borderRadius: BorderRadius.circular(12),
          child: const Icon(Icons.menu_rounded, color: _lightText, size: 22),
        ),
        const SizedBox(width: 14),
        const Text(
          'Expense Audit AI',
          style: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.w700,
            color: _lightText,
          ),
        ),
        const Spacer(),
        Container(
          width: 40,
          height: 40,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            gradient: const LinearGradient(
              colors: [Color(0xFF60A5FA), Color(0xFF3B82F6)],
            ),
            border: Border.all(color: Colors.white, width: 2),
            boxShadow: [
              BoxShadow(
                color: _primaryBlue.withValues(alpha: 0.3),
                blurRadius: 10,
                offset: const Offset(0, 3),
              ),
            ],
          ),
          child: const Icon(Icons.person_rounded, color: Colors.white, size: 20),
        ),
      ],
    );
  }

  // ── Greeting ─────────────────────────────────────────────────────────────────

  Widget _buildGreeting() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Hello, Finance Lead',
          style: TextStyle(
            fontSize: 26,
            fontWeight: FontWeight.w800,
            color: _lightText,
            height: 1.2,
          ),
        ),
        const SizedBox(height: 6),
        Text(
          'Ready to audit today\'s transactions?',
          style: TextStyle(
            fontSize: 15,
            color: _subtitleGrey,
            fontWeight: FontWeight.w400,
          ),
        ),
      ],
    );
  }

  // ── Upload Card ──────────────────────────────────────────────────────────────

  Widget _buildUploadCard() {
    return GestureDetector(
      onTap: _pickAndAnalyze,
      child: GlassContainer(
        width: double.infinity,
        padding: const EdgeInsets.symmetric(vertical: 36, horizontal: 24),
        borderRadius: BorderRadius.circular(24),
        child: Column(
          children: [
            Container(
              padding: const EdgeInsets.all(18),
              decoration: BoxDecoration(
                color: _primaryBlue.withValues(alpha: 0.2),
                shape: BoxShape.circle,
                border: Border.all(color: _primaryBlue.withValues(alpha: 0.5)),
              ),
              child: Icon(
                Icons.cloud_upload_rounded,
                color: _primaryBlue,
                size: 32,
              ),
            ),
            const SizedBox(height: 18),
            const Text(
              'Tap to Upload',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.w700,
                color: _lightText,
              ),
            ),
            const SizedBox(height: 6),
            Text(
              'Support for CSV, PDF, and Receipt Photos',
              style: TextStyle(
                fontSize: 13,
                color: _subtitleGrey,
              ),
            ),
          ],
        ),
      ),
    );
  }

  // ── Analyze Button ───────────────────────────────────────────────────────────

  Widget _buildAnalyzeButton() {
    return SizedBox(
      width: double.infinity,
      height: 56,
      child: ElevatedButton.icon(
        onPressed: _pickAndAnalyze,
        icon: const Icon(Icons.auto_awesome_rounded, size: 22),
        label: const Text(
          'Analyze Expenses',
          style: TextStyle(
            fontSize: 17,
            fontWeight: FontWeight.w700,
            letterSpacing: 0.3,
          ),
        ),
        style: ElevatedButton.styleFrom(
          backgroundColor: _primaryBlue,
          foregroundColor: Colors.white,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
          ),
          elevation: 4,
          shadowColor: _primaryBlue.withValues(alpha: 0.4),
        ),
      ),
    );
  }

  // ── Recent Reports ───────────────────────────────────────────────────────────

  Widget _buildRecentReportsSection() {
    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const Text(
              'Recent Reports',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.w700,
                color: _lightText,
              ),
            ),
            if (_recentReports.isNotEmpty)
              GestureDetector(
                onTap: () => setState(() => _currentNavIndex = 2),
                child: Text(
                  'SEE ALL',
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.w700,
                    color: _primaryBlue,
                    letterSpacing: 0.8,
                  ),
                ),
              ),
          ],
        ),
        const SizedBox(height: 16),
        if (_recentReports.isEmpty)
          _buildEmptyReports()
        else
          ..._recentReports.map((report) => _buildReportTile(report)),
      ],
    );
  }

  Widget _buildEmptyReports() {
    return GlassContainer(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(vertical: 40, horizontal: 24),
      borderRadius: BorderRadius.circular(20),
      child: Column(
        children: [
          Icon(Icons.description_outlined, size: 48, color: _subtitleGrey.withValues(alpha: 0.4)),
          const SizedBox(height: 12),
          Text(
            'No reports yet',
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.w600,
              color: _subtitleGrey,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            'Upload a CSV to generate your first audit',
            style: TextStyle(
              fontSize: 13,
              color: _subtitleGrey.withValues(alpha: 0.7),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildReportTile(Map<String, dynamic> report) {
    final title = report['title'] as String;
    final date = report['date'] as DateTime;
    final items = report['items'] as int;
    final status = report['status'] as String;
    final isFlagged = status == 'Flagged';

    // Random icon color per tile
    final iconColors = [
      const Color(0xFF7C3AED),
      const Color(0xFF2563EB),
      const Color(0xFFDB2777),
      const Color(0xFF059669),
    ];
    final iconColor = iconColors[_recentReports.indexOf(report) % iconColors.length];

    return GestureDetector(
      onTap: () {
        _openReportFromDashboard(report);
      },
      child: GlassContainer(
        margin: const EdgeInsets.only(bottom: 12),
        padding: const EdgeInsets.all(16),
        borderRadius: BorderRadius.circular(18),
        child: Row(
          children: [
            // Circular icon
            Container(
              width: 44,
              height: 44,
              decoration: BoxDecoration(
                color: iconColor.withValues(alpha: 0.1),
                shape: BoxShape.circle,
              ),
              child: Icon(
                Icons.description_outlined,
                color: iconColor,
                size: 22,
              ),
            ),
            const SizedBox(width: 14),
            // Title + subtitle
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: const TextStyle(
                      fontWeight: FontWeight.w600,
                      fontSize: 15,
                      color: _lightText,
                    ),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                  const SizedBox(height: 3),
                  Text(
                    '${_formatDate(date)} • $items ITEMS',
                    style: TextStyle(
                      fontSize: 12,
                      color: _subtitleGrey,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ],
              ),
            ),
            // Status badge
            Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(
                  isFlagged ? Icons.warning_amber_rounded : Icons.check_circle,
                  size: 14,
                  color: isFlagged ? const Color(0xFFEF4444) : const Color(0xFF10B981),
                ),
                const SizedBox(width: 4),
                Text(
                  status,
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.w700,
                    color: isFlagged ? const Color(0xFFEF4444) : const Color(0xFF10B981),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  // ── Bottom Navigation ────────────────────────────────────────────────────────

  Widget _buildBottomNav() {
    return SafeArea(
      child: Padding(
        padding: const EdgeInsets.fromLTRB(20, 0, 20, 16),
        child: GlassContainer(
          borderRadius: BorderRadius.circular(28),
          padding: const EdgeInsets.symmetric(vertical: 12),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            mainAxisSize: MainAxisSize.min,
            children: [
              _buildNavItem(Icons.home_rounded, 'Overview', 0),
              _buildNavItem(Icons.analytics_rounded, 'Audits', 1),
              _buildNavItem(Icons.bar_chart_rounded, 'Reports', 2),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildNavItem(IconData icon, String label, int index) {
    final isActive = _currentNavIndex == index;
    final color = isActive ? _primaryBlue : const Color(0xFF9CA3AF);
    return GestureDetector(
      onTap: () {
        setState(() => _currentNavIndex = index);
        // Show snackbar when Audits is clicked
        if (index == 1) {
          ScaffoldMessenger.of(context).showSnackBar(
            AppSnackbar.info('Upload a CSV file to audit'),
          );
        }
      },
      behavior: HitTestBehavior.opaque,
      child: SizedBox(
        width: 64,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, color: color, size: 24),
            const SizedBox(height: 4),
            Text(
              label,
              style: TextStyle(
                color: color,
                fontSize: 11,
                fontWeight: isActive ? FontWeight.w700 : FontWeight.w500,
              ),
            ),
            if (isActive) ...[
              const SizedBox(height: 4),
              Container(
                width: 5,
                height: 5,
                decoration: BoxDecoration(
                  color: _primaryBlue,
                  shape: BoxShape.circle,
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
