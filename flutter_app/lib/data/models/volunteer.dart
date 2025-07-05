import 'package:json_annotation/json_annotation.dart';

part 'volunteer.g.dart';

@JsonSerializable()
class Volunteer {
  final int? id;
  final String name;
  final String? phone;
  final String? email;
  final String? address;
  final String? skills;
  final String? notes;
  final bool isActive;
  final DateTime? dateJoined;
  final DateTime? createdAt;
  final DateTime? updatedAt;

  const Volunteer({
    this.id,
    required this.name,
    this.phone,
    this.email,
    this.address,
    this.skills,
    this.notes,
    this.isActive = true,
    this.dateJoined,
    this.createdAt,
    this.updatedAt,
  });

  factory Volunteer.fromJson(Map<String, dynamic> json) => _$VolunteerFromJson(json);
  Map<String, dynamic> toJson() => _$VolunteerToJson(this);

  // Convert from database map
  factory Volunteer.fromMap(Map<String, dynamic> map) {
    return Volunteer(
      id: map['id'] as int?,
      name: map['name'] as String,
      phone: map['phone'] as String?,
      email: map['email'] as String?,
      address: map['address'] as String?,
      skills: map['skills'] as String?,
      notes: map['notes'] as String?,
      isActive: (map['is_active'] as int?) == 1,
      dateJoined: _parseDateTime(map['date_joined']),
      createdAt: _parseDateTime(map['created_at']),
      updatedAt: _parseDateTime(map['updated_at']),
    );
  }

  // Helper method to parse DateTime from either int (milliseconds) or String
  static DateTime? _parseDateTime(dynamic value) {
    if (value == null) return null;
    if (value is int) {
      return DateTime.fromMillisecondsSinceEpoch(value);
    }
    if (value is String) {
      return DateTime.parse(value);
    }
    return null;
  }

  // Convert to database map
  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'name': name,
      'phone': phone,
      'email': email,
      'address': address,
      'skills': skills,
      'notes': notes,
      'is_active': isActive ? 1 : 0,
      'date_joined': dateJoined?.toIso8601String(),
      'created_at': createdAt?.toIso8601String(),
      'updated_at': updatedAt?.toIso8601String(),
    };
  }

  // Create a copy with updated fields
  Volunteer copyWith({
    int? id,
    String? name,
    String? phone,
    String? email,
    String? address,
    String? skills,
    String? notes,
    bool? isActive,
    DateTime? dateJoined,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return Volunteer(
      id: id ?? this.id,
      name: name ?? this.name,
      phone: phone ?? this.phone,
      email: email ?? this.email,
      address: address ?? this.address,
      skills: skills ?? this.skills,
      notes: notes ?? this.notes,
      isActive: isActive ?? this.isActive,
      dateJoined: dateJoined ?? this.dateJoined,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }

  @override
  String toString() {
    return 'Volunteer(id: $id, name: $name, email: $email, isActive: $isActive)';
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is Volunteer && other.id == id;
  }

  @override
  int get hashCode => id.hashCode;
}
