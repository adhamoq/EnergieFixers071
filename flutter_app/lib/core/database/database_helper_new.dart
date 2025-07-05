import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:sqflite/sqflite.dart';
import 'package:sqflite_common_ffi/sqflite_ffi.dart';
import 'package:path/path.dart';
import 'package:path_provider/path_provider.dart';
import 'package:sqflite_common/sqlite_api.dart';


// Cross-platform database helper supporting both web and Windows
class DatabaseHelper {
  static final DatabaseHelper _instance = DatabaseHelper._internal();
  factory DatabaseHelper() => _instance;
  DatabaseHelper._internal();
  static DatabaseHelper get instance => _instance;

  static Database? _database;

  Future<Database> get database async {
    if (_database != null) return _database!;
    
    if (kIsWeb) {
      // For web, use in-memory database
      _database = await _initWebDatabase();
    } else {
      // For Windows/Desktop, use SQLite file
      _database = await _initWindowsDatabase();
    }
    return _database!;
  }

  Future<Database> _initWebDatabase() async {
    // For web, use in-memory database with sqflite_common_ffi
    databaseFactory = databaseFactoryFfi;
    final db = await openDatabase(
      inMemoryDatabasePath,
      version: 1,
      onCreate: _onCreate,
    );
    await _insertSampleData(db);
    return db;
  }

  Future<Database> _initWindowsDatabase() async {
    // Initialize FFI for Windows
    sqfliteFfiInit();
    databaseFactory = databaseFactoryFfi;

    // Get the application documents directory
    final directory = await getApplicationDocumentsDirectory();
    final path = join(directory.path, 'energiefixers071.db');
    
    final db = await openDatabase(
      path,
      version: 1,
      onCreate: _onCreate,
    );
    
    // Check if we need to insert sample data
    final existingVolunteers = await db.query('volunteers');
    if (existingVolunteers.isEmpty) {
      await _insertSampleData(db);
    }
    
    return db;
  }

  Future<void> _onCreate(Database db, int version) async {
    // Create volunteers table
    await db.execute('''
      CREATE TABLE volunteers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        phone TEXT,
        address TEXT,
        skills TEXT,
        notes TEXT,
        is_active INTEGER DEFAULT 1,
        date_joined TEXT,
        created_at INTEGER,
        updated_at INTEGER
      )
    ''');

    // Create visits table
    await db.execute('''
      CREATE TABLE visits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        volunteer_id INTEGER,
        client_name TEXT,
        address TEXT NOT NULL,
        visit_date INTEGER,
        status TEXT DEFAULT 'scheduled',
        notes TEXT,
        created_at INTEGER,
        updated_at INTEGER,
        FOREIGN KEY (volunteer_id) REFERENCES volunteers (id)
      )
    ''');

    // Create appointments table
    await db.execute('''
      CREATE TABLE appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        client_name TEXT,
        date INTEGER,
        volunteer_id INTEGER,
        status TEXT DEFAULT 'confirmed',
        created_at INTEGER,
        FOREIGN KEY (volunteer_id) REFERENCES volunteers (id)
      )
    ''');
  }

  Future<void> _insertSampleData(Database db) async {
    final now = DateTime.now().millisecondsSinceEpoch;
    
    // Insert sample volunteers
    await db.insert('volunteers', {
      'name': 'John Doe',
      'email': 'john.doe@example.com',
      'phone': '+31 6 12345678',
      'address': 'Amsterdam, Netherlands',
      'skills': 'Insulation, Heating',
      'is_active': 1,
      'created_at': now,
      'updated_at': now,
    });

    await db.insert('volunteers', {
      'name': 'Jane Smith',
      'email': 'jane.smith@example.com',
      'phone': '+31 6 87654321',
      'address': 'Utrecht, Netherlands',
      'skills': 'Solar panels, Ventilation',
      'is_active': 1,
      'created_at': now,
      'updated_at': now,
    });

    // Insert sample visit
    await db.insert('visits', {
      'volunteer_id': 1,
      'client_name': 'Family Johnson',
      'address': 'Main Street 123, Amsterdam',
      'visit_date': DateTime.now().add(Duration(days: 3)).millisecondsSinceEpoch,
      'status': 'scheduled',
      'created_at': now,
      'updated_at': now,
    });

    // Insert sample appointment
    await db.insert('appointments', {
      'title': 'Energy Consultation',
      'client_name': 'Johnson Family',
      'date': DateTime.now().add(Duration(days: 2)).millisecondsSinceEpoch,
      'volunteer_id': 1,
      'status': 'confirmed',
      'created_at': now,
    });
  }

  // CRUD operations using SQL queries
  Future<List<Map<String, dynamic>>> getVolunteers() async {
    final db = await database;
    return await db.query('volunteers', orderBy: 'name ASC');
  }

  Future<List<Map<String, dynamic>>> getVisits() async {
    final db = await database;
    return await db.query('visits', orderBy: 'visit_date DESC');
  }

  Future<List<Map<String, dynamic>>> getAppointments() async {
    final db = await database;
    return await db.query('appointments', orderBy: 'date DESC');
  }

  Future<int> insertVolunteer(Map<String, dynamic> volunteer) async {
    final db = await database;
    volunteer['created_at'] = DateTime.now().millisecondsSinceEpoch;
    volunteer['updated_at'] = DateTime.now().millisecondsSinceEpoch;
    return await db.insert('volunteers', volunteer);
  }

  Future<int> insertVisit(Map<String, dynamic> visit) async {
    final db = await database;
    visit['created_at'] = DateTime.now().millisecondsSinceEpoch;
    visit['updated_at'] = DateTime.now().millisecondsSinceEpoch;
    return await db.insert('visits', visit);
  }

  Future<int> insertAppointment(Map<String, dynamic> appointment) async {
    final db = await database;
    appointment['created_at'] = DateTime.now().millisecondsSinceEpoch;
    return await db.insert('appointments', appointment);
  }

  Future<void> updateVolunteer(Map<String, dynamic> volunteer) async {
    final db = await database;
    volunteer['updated_at'] = DateTime.now().millisecondsSinceEpoch;
    await db.update(
      'volunteers', 
      volunteer, 
      where: 'id = ?', 
      whereArgs: [volunteer['id']]
    );
  }

  Future<void> deleteVolunteer(int id) async {
    final db = await database;
    await db.delete('volunteers', where: 'id = ?', whereArgs: [id]);
  }

  Future<Map<String, int>> getStatistics() async {
    final db = await database;
    
    final volunteerCount = Sqflite.firstIntValue(
      await db.rawQuery('SELECT COUNT(*) FROM volunteers')
    ) ?? 0;
    
    final visitsCount = Sqflite.firstIntValue(
      await db.rawQuery('SELECT COUNT(*) FROM visits')
    ) ?? 0;
    
    final appointmentsCount = Sqflite.firstIntValue(
      await db.rawQuery('SELECT COUNT(*) FROM appointments')
    ) ?? 0;

    final completedVisits = Sqflite.firstIntValue(
      await db.rawQuery("SELECT COUNT(*) FROM visits WHERE status = 'completed'")
    ) ?? 0;

    return {
      'volunteers': volunteerCount,
      'visits': visitsCount,
      'appointments': appointmentsCount,
      'completed_visits': completedVisits,
    };
  }

  Future<void> close() async {
    final db = await database;
    await db.close();
  }
}
