import 'package:flutter/material.dart';
import 'dart:async';
import 'dart:math' as math;
import 'audit_report_screen.dart';
import '../widgets/app_snackbar.dart';
import '../widgets/glass_container.dart';

class AuditLoadingScreen extends StatefulWidget {
  /// The future that resolves with the backend analysis result.
  final Future<Map<String, dynamic>?> analysisFuture;
  final String fileName;

  const AuditLoadingScreen({
    super.key,
    required this.analysisFuture,
    required this.fileName,
  });

  @override
  State<AuditLoadingScreen> createState() => _AuditLoadingScreenState();
}

class _AuditLoadingScreenState extends State<AuditLoadingScreen>
    with TickerProviderStateMixin {
  // Animation controllers
  late AnimationController _pulseController;
  late Animation<double> _pulseAnimation;
  late AnimationController _rotateController;
  late AnimationController _waveController;
  late AnimationController _fadeInController;
  late Animation<double> _fadeInAnimation;
  late AnimationController _shimmerController;

  double _progress = 0.0;
  int _currentStep = 0;
  int _estimatedSeconds = 20;
  Timer? _progressTimer;
  Timer? _estimateTimer;
  bool _backendDone = false;
  Map<String, dynamic>? _result;

  final List<Map<String, String>> _steps = [
    {'title': 'Extracting data', 'subtitle': 'OCR processing...'},
    {'title': 'Scanning policy engine', 'subtitle': 'Checking corporate compliance'},
    {'title': 'AI Anomaly detection', 'subtitle': 'Analyzing patterns...'},
    {'title': 'Generating report', 'subtitle': 'Finalizing results'},
  ];

  @override
  void initState() {
    super.initState();

    // Fade-in for the whole screen
    _fadeInController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 800),
    );
    _fadeInAnimation = CurvedAnimation(parent: _fadeInController, curve: Curves.easeOut);
    _fadeInController.forward();

    // Pulse animation for the central icon
    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 2400),
    )..repeat(reverse: true);
    _pulseAnimation = Tween<double>(begin: 1.0, end: 1.1).animate(
      CurvedAnimation(parent: _pulseController, curve: Curves.easeInOut),
    );

    // Rotation for dashed rings
    _rotateController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 5),
    )..repeat();

    // Wave bars animation
    _waveController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1200),
    )..repeat(reverse: true);

    // Shimmer for progress bar
    _shimmerController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 2000),
    )..repeat();

    _startProgressSimulation();
    _startEstimateCountdown();
    _listenToBackend();
  }

  void _listenToBackend() {
    widget.analysisFuture.then((result) {
      _backendDone = true;
      _result = result;
      // Animate progress to 100%
      _progressTimer?.cancel();
      _estimateTimer?.cancel();
      _animateToComplete();
    }).catchError((e) {
      _backendDone = true;
      _result = null;
      _progressTimer?.cancel();
      _estimateTimer?.cancel();
      if (mounted) {
        Navigator.of(context).pop();
        ScaffoldMessenger.of(context).showSnackBar(
          AppSnackbar.error('Analysis failed: $e'),
        );
      }
    });
  }

  void _animateToComplete() {
    const interval = Duration(milliseconds: 70);
    _progressTimer = Timer.periodic(interval, (timer) {
      if (!mounted) { timer.cancel(); return; }
      setState(() {
        _progress += 0.04;
        if (_progress >= 1.0) {
          _progress = 1.0;
          _currentStep = _steps.length; // all done
          _estimatedSeconds = 0;
          timer.cancel();
          _navigateToReport();
        } else {
          _currentStep = 3;
        }
      });
    });
  }

  void _navigateToReport() {
    Future.delayed(const Duration(milliseconds: 600), () {
      if (!mounted) return;
      if (_result != null && _result!['status'] == 'success') {
        final report = _result!['report'] ?? {};
        Navigator.of(context).push(
          PageRouteBuilder(
            pageBuilder: (_, __, ___) => AuditReportScreen(
              reportData: report,
              reportTitle: widget.fileName,
            ),
            transitionsBuilder: (_, animation, __, child) {
              return FadeTransition(
                opacity: animation,
                child: SlideTransition(
                  position: Tween<Offset>(
                    begin: const Offset(0, 0.08),
                    end: Offset.zero,
                  ).animate(CurvedAnimation(parent: animation, curve: Curves.easeOut)),
                  child: child,
                ),
              );
            },
            transitionDuration: const Duration(milliseconds: 500),
          ),
        ).then((_) {
          if (!mounted) return;
          Navigator.of(context).pop(_result);
        });
      } else {
        Navigator.of(context).pop(_result);
      }
    });
  }

  void _startProgressSimulation() {
    const interval = Duration(milliseconds: 200);
    _progressTimer = Timer.periodic(interval, (timer) {
      if (!mounted || _backendDone) { timer.cancel(); return; }
      setState(() {
        // Slow down as we approach 90%
        final remaining = 0.90 - _progress;
        _progress += remaining * 0.012;
        _progress = _progress.clamp(0.0, 0.90);

        if (_progress < 0.25) {
          _currentStep = 0;
        } else if (_progress < 0.50) {
          _currentStep = 1;
        } else if (_progress < 0.75) {
          _currentStep = 2;
        } else {
          _currentStep = 3;
        }
      });
    });
  }

  void _startEstimateCountdown() {
    _estimateTimer = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (!mounted) { timer.cancel(); return; }
      setState(() {
        if (_estimatedSeconds > 2) _estimatedSeconds--;
      });
    });
  }

  @override
  void dispose() {
    _pulseController.dispose();
    _rotateController.dispose();
    _waveController.dispose();
    _fadeInController.dispose();
    _shimmerController.dispose();
    _progressTimer?.cancel();
    _estimateTimer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0B1024),
      extendBody: true,
      extendBodyBehindAppBar: true,
      body: FadeTransition(
        opacity: _fadeInAnimation,
        child: Stack(
          children: [
            Positioned(
              top: -120,
              left: -80,
              child: Container(
                width: 260,
                height: 260,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: const Color(0xFF5C6BC0).withValues(alpha: 0.22),
                  boxShadow: [
                    BoxShadow(
                      color: const Color(0xFF5C6BC0).withValues(alpha: 0.18),
                      blurRadius: 120,
                      spreadRadius: 24,
                    ),
                  ],
                ),
              ),
            ),
            Positioned(
              bottom: 120,
              right: -70,
              child: Container(
                width: 220,
                height: 220,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: const Color(0xFF7C4DFF).withValues(alpha: 0.18),
                  boxShadow: [
                    BoxShadow(
                      color: const Color(0xFF7C4DFF).withValues(alpha: 0.15),
                      blurRadius: 110,
                      spreadRadius: 18,
                    ),
                  ],
                ),
              ),
            ),
            SafeArea(
              child: Column(
                children: [
                  Padding(
                    padding: const EdgeInsets.fromLTRB(16, 8, 16, 0),
                    child: _buildGlassHeader(),
                  ),
                  Expanded(
                    child: SingleChildScrollView(
                      padding: const EdgeInsets.fromLTRB(24.0, 20.0, 24.0, 24.0),
                      child: Column(
                        children: [
                          const SizedBox(height: 12),
                          _buildCentralAnimation(),
                          const SizedBox(height: 34),
                          _buildHeadline(),
                          const SizedBox(height: 10),
                          _buildSubtitle(),
                          const SizedBox(height: 28),
                          _buildProgressSection(),
                          const SizedBox(height: 20),
                          _buildStepsCard(),
                          const SizedBox(height: 20),
                          _buildAIBadge(),
                          const SizedBox(height: 24),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
      bottomNavigationBar: _buildBottomNav(),
    );
  }

  Widget _buildGlassHeader() {
    return GlassContainer(
      blur: 24,
      opacity: 0.08,
      borderRadius: BorderRadius.circular(22),
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
      child: Row(
        children: [
          IconButton(
            icon: const Icon(Icons.menu_rounded, color: Color(0xFFC7D2FE)),
            onPressed: () {},
          ),
          const Expanded(
            child: Center(
              child: Text(
                'Expense Audit AI',
                style: TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.w800,
                  fontSize: 18,
                  letterSpacing: 0.2,
                ),
              ),
            ),
          ),
          Container(
            margin: const EdgeInsets.only(right: 4),
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: Colors.white.withValues(alpha: 0.12),
              border: Border.all(color: Colors.white.withValues(alpha: 0.18)),
            ),
            child: const CircleAvatar(
              radius: 18,
              backgroundColor: Colors.transparent,
              child: Icon(Icons.person_rounded, color: Color(0xFFE0E7FF), size: 22),
            ),
          ),
        ],
      ),
    );
  }

  // ── Central animated icon ──────────────────────────────────────────────────

  Widget _buildCentralAnimation() {
    return Center(
      child: ScaleTransition(
        scale: _pulseAnimation,
        child: SizedBox(
          width: 160,
          height: 160,
          child: Stack(
            alignment: Alignment.center,
            children: [
              // Outer dashed ring (slow rotation)
              AnimatedBuilder(
                animation: _rotateController,
                builder: (_, __) => Transform.rotate(
                  angle: _rotateController.value * 2 * math.pi,
                  child: CustomPaint(
                    size: const Size(156, 156),
                    painter: _DashedCirclePainter(
                      color: const Color(0xFFC5CAE9),
                      dashCount: 28,
                      strokeWidth: 1.2,
                    ),
                  ),
                ),
              ),
              // Inner dashed ring (reverse rotation)
              AnimatedBuilder(
                animation: _rotateController,
                builder: (_, __) => Transform.rotate(
                  angle: -_rotateController.value * 2 * math.pi * 0.7,
                  child: CustomPaint(
                    size: const Size(130, 130),
                    painter: _DashedCirclePainter(
                      color: const Color(0xFF9FA8DA).withValues(alpha: 0.5),
                      dashCount: 20,
                      strokeWidth: 1.0,
                    ),
                  ),
                ),
              ),
              // Glowing background circle
              Container(
                width: 90,
                height: 90,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  gradient: const RadialGradient(
                    colors: [Color(0xFF5C6BC0), Color(0xFF3F51B5)],
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: const Color(0xFF3F51B5).withValues(alpha: 0.35),
                      blurRadius: 28,
                      spreadRadius: 4,
                    ),
                  ],
                ),
              ),
              // Animated waveform bars
              AnimatedBuilder(
                animation: _waveController,
                builder: (_, __) => _WaveformIcon(progress: _waveController.value),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildHeadline() {
    return const Text(
      'Analyzing expenses...',
      textAlign: TextAlign.center,
      style: TextStyle(
        fontSize: 28,
        fontWeight: FontWeight.w900,
        color: Colors.white,
        height: 1.2,
        letterSpacing: -0.3,
      ),
    );
  }

  Widget _buildSubtitle() {
    return Text(
      'Processing ${widget.fileName}',
      textAlign: TextAlign.center,
      style: const TextStyle(fontSize: 14, color: Color(0xFF7986CB), height: 1.5),
    );
  }

  // ── Progress bar with percentage ───────────────────────────────────────────

  Widget _buildProgressSection() {
    return GlassContainer(
      blur: 22,
      opacity: 0.09,
      borderRadius: BorderRadius.circular(22),
      padding: const EdgeInsets.fromLTRB(18, 18, 18, 16),
      child: Column(
        children: [
          ClipRRect(
            borderRadius: BorderRadius.circular(10),
            child: Stack(
              children: [
                Container(
                  height: 10,
                  decoration: BoxDecoration(
                    color: Colors.white.withValues(alpha: 0.09),
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(color: Colors.white.withValues(alpha: 0.08)),
                  ),
                ),
                LayoutBuilder(
                  builder: (context, constraints) => AnimatedContainer(
                    duration: const Duration(milliseconds: 120),
                    height: 10,
                    width: constraints.maxWidth * _progress,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(10),
                      gradient: const LinearGradient(
                        colors: [Color(0xFF5C6BC0), Color(0xFF7C4DFF)],
                      ),
                      boxShadow: [
                        BoxShadow(
                          color: const Color(0xFF7C4DFF).withValues(alpha: 0.22),
                          blurRadius: 18,
                          spreadRadius: 1,
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 12),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                '${(_progress * 100).toInt()}% Processed',
                style: const TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.w700,
                  color: Color(0xFFD6DBFF),
                ),
              ),
              Text(
                'Est. ${_estimatedSeconds}s remaining',
                style: const TextStyle(
                  fontSize: 13,
                  color: Color(0xFFB5C1FF),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  // ── Steps card ─────────────────────────────────────────────────────────────

  Widget _buildStepsCard() {
    return GlassContainer(
      blur: 24,
      opacity: 0.10,
      width: double.infinity,
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 22),
      borderRadius: BorderRadius.circular(22),
      border: Border.all(color: Colors.white.withValues(alpha: 0.14)),
      child: Column(
        children: List.generate(_steps.length, (i) => _buildStepItem(i)),
      ),
    );
  }

  Widget _buildStepItem(int index) {
    final isCompleted = index < _currentStep;
    final isCurrent = index == _currentStep;

    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        SizedBox(
          width: 28,
          child: Column(
            children: [
              _buildStepIcon(isCompleted: isCompleted, isCurrent: isCurrent),
              if (index < _steps.length - 1)
                Padding(
                  padding: const EdgeInsets.symmetric(vertical: 3),
                  child: CustomPaint(
                    size: const Size(1, 24),
                    painter: _DottedLinePainter(
                      color: isCompleted
                          ? const Color(0xFF9FA8DA)
                          : const Color(0xFFE0E0E0),
                    ),
                  ),
                ),
            ],
          ),
        ),
        const SizedBox(width: 14),
        Expanded(
          child: Padding(
            padding: EdgeInsets.only(bottom: index < _steps.length - 1 ? 2 : 0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  _steps[index]['title']!,
                  style: TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.w600,
                    color: isCurrent
                        ? const Color(0xFF7C4DFF)
                        : isCompleted
                            ? Colors.white
                            : const Color(0xFF64748B),
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  isCompleted
                      ? _getCompletedSubtitle(index)
                      : _steps[index]['subtitle']!,
                  style: TextStyle(
                    fontSize: 12,
                    color: isCurrent
                        ? const Color(0xFF9575CD)
                        : isCompleted
                            ? const Color(0xFF757575)
                            : const Color(0xFFBDBDBD),
                  ),
                ),
                const SizedBox(height: 10),
              ],
            ),
          ),
        ),
      ],
    );
  }

  String _getCompletedSubtitle(int index) {
    switch (index) {
      case 0: return 'OCR complete (14 items)';
      case 1: return 'Checking corporate compliance';
      case 2: return 'Patterns analyzed';
      case 3: return 'Report ready';
      default: return 'Done';
    }
  }

  Widget _buildStepIcon({required bool isCompleted, required bool isCurrent}) {
    if (isCompleted) {
      return Container(
        width: 26,
        height: 26,
        decoration: const BoxDecoration(
          shape: BoxShape.circle,
          gradient: LinearGradient(
            colors: [Color(0xFF3F51B5), Color(0xFF5C6BC0)],
          ),
        ),
        child: const Icon(Icons.check_rounded, size: 15, color: Colors.white),
      );
    } else if (isCurrent) {
      return SizedBox(
        width: 26,
        height: 26,
        child: Stack(
          alignment: Alignment.center,
          children: [
            AnimatedBuilder(
              animation: _rotateController,
              builder: (_, __) => Transform.rotate(
                angle: _rotateController.value * 2 * math.pi,
                child: CustomPaint(
                  size: const Size(26, 26),
                  painter: _DashedCirclePainter(
                    color: const Color(0xFF7C4DFF),
                    dashCount: 14,
                    strokeWidth: 1.5,
                  ),
                ),
              ),
            ),
            Container(
              width: 16,
              height: 16,
              decoration: const BoxDecoration(
                shape: BoxShape.circle,
                color: Color(0xFFEDE7F6),
              ),
              child: const Icon(Icons.sync, size: 10, color: Color(0xFF7C4DFF)),
            ),
          ],
        ),
      );
    } else {
      return Container(
        width: 26,
        height: 26,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          border: Border.all(color: const Color(0xFFE0E0E0), width: 1.5),
          color: Colors.white,
        ),
        child: Center(
          child: Container(
            width: 6,
            height: 6,
            decoration: const BoxDecoration(
              shape: BoxShape.circle,
              color: Color(0xFFE0E0E0),
            ),
          ),
        ),
      );
    }
  }

  // ── AI Engine badge ────────────────────────────────────────────────────────

  Widget _buildAIBadge() {
    return AnimatedBuilder(
      animation: _pulseController,
      builder: (_, __) {
        final glow = 0.1 + (_pulseController.value * 0.15);
        return GlassContainer(
          blur: 22,
          opacity: 0.08,
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
          borderRadius: BorderRadius.circular(30),
          border: Border.all(color: Colors.white.withValues(alpha: 0.12)),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Container(
                width: 8,
                height: 8,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: const Color(0xFF7C4DFF),
                  boxShadow: [
                    BoxShadow(
                      color: const Color(0xFF7C4DFF).withValues(alpha: glow),
                      blurRadius: 6,
                    ),
                  ],
                ),
              ),
              const SizedBox(width: 10),
              const Text(
                'AI ENGINE V2.4 ACTIVE',
                style: TextStyle(
                  fontSize: 11,
                  fontWeight: FontWeight.w700,
                  color: Color(0xFF5C6BC0),
                  letterSpacing: 1.2,
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  // ── Bottom nav ─────────────────────────────────────────────────────────────

  Widget _buildBottomNav() {
    return SafeArea(
      top: false,
      child: Padding(
        padding: const EdgeInsets.fromLTRB(16, 0, 16, 14),
        child: GlassContainer(
          blur: 26,
          opacity: 0.10,
          borderRadius: BorderRadius.circular(22),
          padding: const EdgeInsets.symmetric(vertical: 12),
          border: Border.all(color: Colors.white.withValues(alpha: 0.12)),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              _buildNavItem(icon: Icons.dashboard_rounded, label: 'Overview', isActive: false),
              _buildNavItem(icon: Icons.analytics_rounded, label: 'Audits', isActive: true),
              _buildNavItem(icon: Icons.bar_chart_rounded, label: 'Reports', isActive: false),
              _buildNavItem(icon: Icons.settings_rounded, label: 'Settings', isActive: false),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildNavItem({required IconData icon, required String label, required bool isActive}) {
    final color = isActive ? const Color(0xFFE0E7FF) : const Color(0xFF94A3B8);
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        if (isActive)
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: const Color(0xFF6D5EF6).withValues(alpha: 0.8),
              borderRadius: BorderRadius.circular(10),
              boxShadow: [
                BoxShadow(
                  color: const Color(0xFF7C4DFF).withValues(alpha: 0.28),
                  blurRadius: 14,
                  spreadRadius: 1,
                ),
              ],
            ),
            child: Icon(icon, color: Colors.white, size: 20),
          )
        else
          Padding(
            padding: const EdgeInsets.all(8),
            child: Icon(icon, color: color, size: 22),
          ),
        const SizedBox(height: 4),
        Text(
          label,
          style: TextStyle(
            color: color,
            fontSize: 10,
            fontWeight: isActive ? FontWeight.w700 : FontWeight.w500,
          ),
        ),
      ],
    );
  }
}

// ── Custom Painters ──────────────────────────────────────────────────────────

class _DashedCirclePainter extends CustomPainter {
  final Color color;
  final int dashCount;
  final double strokeWidth;

  _DashedCirclePainter({
    required this.color,
    required this.dashCount,
    required this.strokeWidth,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = color
      ..strokeWidth = strokeWidth
      ..strokeCap = StrokeCap.round
      ..style = PaintingStyle.stroke;

    final center = Offset(size.width / 2, size.height / 2);
    final radius = (size.width / 2) - strokeWidth;
    final dashAngle = (2 * math.pi) / (dashCount * 2);

    for (int i = 0; i < dashCount; i++) {
      final startAngle = i * 2 * dashAngle;
      canvas.drawArc(
        Rect.fromCircle(center: center, radius: radius),
        startAngle,
        dashAngle,
        false,
        paint,
      );
    }
  }

  @override
  bool shouldRepaint(_DashedCirclePainter old) =>
      old.color != color || old.dashCount != dashCount;
}

class _DottedLinePainter extends CustomPainter {
  final Color color;
  _DottedLinePainter({required this.color});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = color
      ..strokeWidth = 1.5
      ..strokeCap = StrokeCap.round;

    const dotRadius = 1.2;
    const spacing = 5.0;
    double y = 0;
    while (y < size.height) {
      canvas.drawCircle(Offset(size.width / 2, y), dotRadius, paint);
      y += spacing;
    }
  }

  @override
  bool shouldRepaint(_DottedLinePainter old) => old.color != color;
}

class _WaveformIcon extends StatelessWidget {
  final double progress;
  const _WaveformIcon({required this.progress});

  @override
  Widget build(BuildContext context) {
    const barCount = 5;

    return Row(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: List.generate(barCount, (i) {
        final phase = (i / barCount) * math.pi;
        final height = 24.0 * (0.35 + 0.65 * ((math.sin(progress * math.pi + phase) + 1) / 2));

        return Container(
          margin: const EdgeInsets.symmetric(horizontal: 2.2),
          width: 4,
          height: height,
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(4),
          ),
        );
      }),
    );
  }
}
