import 'package:flutter/material.dart';

class AppTheme {
  // Brand colors (same as your Python app)
  static const Color primaryGreen = Color(0xFF1D8420);
  static const Color secondaryYellow = Color(0xFFF9C440);
  
  // Light theme colors (matching your flatly theme)
  static const Color lightPrimary = Color(0xFF2c3e50);
  static const Color lightSecondary = Color(0xFF95a5a6);
  static const Color lightSuccess = Color(0xFF18bc9c);
  static const Color lightInfo = Color(0xFF3498db);
  static const Color lightWarning = Color(0xFFf39c12);
  static const Color lightDanger = Color(0xFFe74c3c);
  static const Color lightBackground = Color(0xFFf8f9fa);
  static const Color lightSurface = Color(0xFFf1f3f4);
  static const Color lightSidebarBg = Color(0xFFe9ecef);
  
  // Dark theme colors (matching your darkly theme)
  static const Color darkPrimary = Color(0xFF375a7f);
  static const Color darkSecondary = Color(0xFF444444);
  static const Color darkSuccess = Color(0xFF00bc8c);
  static const Color darkInfo = Color(0xFF3498db);
  static const Color darkWarning = Color(0xFFf39c12);
  static const Color darkDanger = Color(0xFFe74c3c);
  static const Color darkBackground = Color(0xFF222222);
  static const Color darkSurface = Color(0xFF303030);
  static const Color darkSidebarBg = Color(0xFF2b2b2b);
  
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      colorScheme: ColorScheme.fromSeed(
        seedColor: primaryGreen,
        brightness: Brightness.light,
        primary: primaryGreen,
        secondary: lightSecondary,
        surface: lightSurface,
        background: lightBackground,
        error: lightDanger,
      ),
      
      // App Bar
      appBarTheme: const AppBarTheme(
        backgroundColor: lightSidebarBg,
        foregroundColor: Colors.black87,
        elevation: 0,
        centerTitle: false,
        titleTextStyle: TextStyle(
          fontFamily: 'SegoeUI',
          fontSize: 20,
          fontWeight: FontWeight.bold,
          color: Colors.black87,
        ),
      ),
      
      // Card theme
      cardTheme: CardThemeData(
        color: Colors.white,
        elevation: 2,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
      ),
      
      // Text theme
      textTheme: const TextTheme(
        displayLarge: TextStyle(fontFamily: 'SegoeUI', fontSize: 32, fontWeight: FontWeight.bold),
        displayMedium: TextStyle(fontFamily: 'SegoeUI', fontSize: 28, fontWeight: FontWeight.bold),
        displaySmall: TextStyle(fontFamily: 'SegoeUI', fontSize: 24, fontWeight: FontWeight.bold),
        headlineLarge: TextStyle(fontFamily: 'SegoeUI', fontSize: 22, fontWeight: FontWeight.bold),
        headlineMedium: TextStyle(fontFamily: 'SegoeUI', fontSize: 20, fontWeight: FontWeight.bold),
        headlineSmall: TextStyle(fontFamily: 'SegoeUI', fontSize: 18, fontWeight: FontWeight.bold),
        titleLarge: TextStyle(fontFamily: 'SegoeUI', fontSize: 16, fontWeight: FontWeight.w600),
        titleMedium: TextStyle(fontFamily: 'SegoeUI', fontSize: 14, fontWeight: FontWeight.w500),
        titleSmall: TextStyle(fontFamily: 'SegoeUI', fontSize: 12, fontWeight: FontWeight.w500),
        bodyLarge: TextStyle(fontFamily: 'SegoeUI', fontSize: 16),
        bodyMedium: TextStyle(fontFamily: 'SegoeUI', fontSize: 14),
        bodySmall: TextStyle(fontFamily: 'SegoeUI', fontSize: 12),
        labelLarge: TextStyle(fontFamily: 'SegoeUI', fontSize: 14, fontWeight: FontWeight.w500),
        labelMedium: TextStyle(fontFamily: 'SegoeUI', fontSize: 12, fontWeight: FontWeight.w500),
        labelSmall: TextStyle(fontFamily: 'SegoeUI', fontSize: 10, fontWeight: FontWeight.w500),
      ),
      
      // Input decoration
      inputDecorationTheme: InputDecorationTheme(
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
        ),
        filled: true,
        fillColor: Colors.white,
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      ),
      
      // Elevated button
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primaryGreen,
          foregroundColor: Colors.white,
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
      ),
      
      // Navigation drawer
      drawerTheme: const DrawerThemeData(
        backgroundColor: lightSidebarBg,
        scrimColor: Colors.black54,
      ),
      
      // Data table
      dataTableTheme: const DataTableThemeData(
        columnSpacing: 16,
        horizontalMargin: 16,
        headingRowColor: MaterialStatePropertyAll(lightSidebarBg),
        dataRowMinHeight: 48,
        dataRowMaxHeight: 56,
      ),
    );
  }
  
  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      colorScheme: ColorScheme.fromSeed(
        seedColor: primaryGreen,
        brightness: Brightness.dark,
        primary: primaryGreen,
        secondary: darkSecondary,
        surface: darkSurface,
        background: darkBackground,
        error: darkDanger,
      ),
      
      // App Bar
      appBarTheme: const AppBarTheme(
        backgroundColor: darkSidebarBg,
        foregroundColor: Colors.white,
        elevation: 0,
        centerTitle: false,
        titleTextStyle: TextStyle(
          fontFamily: 'SegoeUI',
          fontSize: 20,
          fontWeight: FontWeight.bold,
          color: Colors.white,
        ),
      ),
      
      // Card theme
      cardTheme: CardThemeData(
        color: darkSurface,
        elevation: 2,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
      ),
      
      // Text theme (same structure as light but will inherit dark colors)
      textTheme: const TextTheme(
        displayLarge: TextStyle(fontFamily: 'SegoeUI', fontSize: 32, fontWeight: FontWeight.bold),
        displayMedium: TextStyle(fontFamily: 'SegoeUI', fontSize: 28, fontWeight: FontWeight.bold),
        displaySmall: TextStyle(fontFamily: 'SegoeUI', fontSize: 24, fontWeight: FontWeight.bold),
        headlineLarge: TextStyle(fontFamily: 'SegoeUI', fontSize: 22, fontWeight: FontWeight.bold),
        headlineMedium: TextStyle(fontFamily: 'SegoeUI', fontSize: 20, fontWeight: FontWeight.bold),
        headlineSmall: TextStyle(fontFamily: 'SegoeUI', fontSize: 18, fontWeight: FontWeight.bold),
        titleLarge: TextStyle(fontFamily: 'SegoeUI', fontSize: 16, fontWeight: FontWeight.w600),
        titleMedium: TextStyle(fontFamily: 'SegoeUI', fontSize: 14, fontWeight: FontWeight.w500),
        titleSmall: TextStyle(fontFamily: 'SegoeUI', fontSize: 12, fontWeight: FontWeight.w500),
        bodyLarge: TextStyle(fontFamily: 'SegoeUI', fontSize: 16),
        bodyMedium: TextStyle(fontFamily: 'SegoeUI', fontSize: 14),
        bodySmall: TextStyle(fontFamily: 'SegoeUI', fontSize: 12),
        labelLarge: TextStyle(fontFamily: 'SegoeUI', fontSize: 14, fontWeight: FontWeight.w500),
        labelMedium: TextStyle(fontFamily: 'SegoeUI', fontSize: 12, fontWeight: FontWeight.w500),
        labelSmall: TextStyle(fontFamily: 'SegoeUI', fontSize: 10, fontWeight: FontWeight.w500),
      ),
      
      // Input decoration
      inputDecorationTheme: InputDecorationTheme(
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
        ),
        filled: true,
        fillColor: const Color(0xFF495057),
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      ),
      
      // Elevated button
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primaryGreen,
          foregroundColor: Colors.white,
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
      ),
      
      // Navigation drawer
      drawerTheme: const DrawerThemeData(
        backgroundColor: darkSidebarBg,
        scrimColor: Colors.black87,
      ),
      
      // Data table
      dataTableTheme: const DataTableThemeData(
        columnSpacing: 16,
        horizontalMargin: 16,
        headingRowColor: MaterialStatePropertyAll(darkSidebarBg),
        dataRowMinHeight: 48,
        dataRowMaxHeight: 56,
      ),
    );
  }
}
