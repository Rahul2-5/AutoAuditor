import 'package:flutter/material.dart';

class AppSnackbar {
  static SnackBar success(String message) {
    return SnackBar(
      behavior: SnackBarBehavior.floating,
      backgroundColor: const Color(0xFFDCFCE7).withValues(alpha: 0.96),
      content: Text(
        message,
        style: const TextStyle(
          color: Color(0xFF14532D),
          fontSize: 14,
          fontWeight: FontWeight.w600,
        ),
      ),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: BorderSide(color: const Color(0xFF86EFAC).withValues(alpha: 0.9)),
      ),
      elevation: 10,
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
    );
  }

  static SnackBar error(String message) {
    return SnackBar(
      behavior: SnackBarBehavior.floating,
      backgroundColor: const Color(0xFFFFE4E6).withValues(alpha: 0.96),
      content: Text(
        message,
        style: const TextStyle(
          color: Color(0xFF7F1D1D),
          fontSize: 14,
          fontWeight: FontWeight.w600,
        ),
      ),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: BorderSide(color: const Color(0xFFFCA5A5).withValues(alpha: 0.9)),
      ),
      elevation: 10,
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
    );
  }

  static SnackBar info(String message) {
    return SnackBar(
      behavior: SnackBarBehavior.floating,
      backgroundColor: const Color(0xFFEFF6FF).withValues(alpha: 0.96),
      content: Text(
        message,
        style: const TextStyle(
          color: Color(0xFF1E3A8A),
          fontSize: 14,
          fontWeight: FontWeight.w600,
        ),
      ),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: BorderSide(color: const Color(0xFF93C5FD).withValues(alpha: 0.9)),
      ),
      elevation: 10,
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
    );
  }
}
