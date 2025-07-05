// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'volunteer.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

Volunteer _$VolunteerFromJson(Map<String, dynamic> json) => Volunteer(
      id: (json['id'] as num?)?.toInt(),
      name: json['name'] as String,
      phone: json['phone'] as String?,
      email: json['email'] as String?,
      address: json['address'] as String?,
      skills: json['skills'] as String?,
      notes: json['notes'] as String?,
      isActive: json['isActive'] as bool? ?? true,
      dateJoined: json['dateJoined'] == null
          ? null
          : DateTime.parse(json['dateJoined'] as String),
      createdAt: json['createdAt'] == null
          ? null
          : DateTime.parse(json['createdAt'] as String),
      updatedAt: json['updatedAt'] == null
          ? null
          : DateTime.parse(json['updatedAt'] as String),
    );

Map<String, dynamic> _$VolunteerToJson(Volunteer instance) => <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'phone': instance.phone,
      'email': instance.email,
      'address': instance.address,
      'skills': instance.skills,
      'notes': instance.notes,
      'isActive': instance.isActive,
      'dateJoined': instance.dateJoined?.toIso8601String(),
      'createdAt': instance.createdAt?.toIso8601String(),
      'updatedAt': instance.updatedAt?.toIso8601String(),
    };
