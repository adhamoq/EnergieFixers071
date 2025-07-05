import 'package:json_annotation/json_annotation.dart';

part 'visit.g.dart';

@JsonSerializable()
class Visit {
  final int? id;
  final int? volunteerId;
  final int? volunteer2Id;
  final String address;
  final DateTime visitDate;
  final DateTime? startTime;
  final DateTime? endTime;
  final String? appointmentTime;
  
  // Resident Information
  final int residentsCount;
  final bool energyMeasuresTaken;
  final String? whichMeasures;
  final bool ventilationChecked;
  
  // Energy Contract Information
  final bool energyUsageChecked;
  final String? contractDuration;
  final double? electricityConsumption;
  final double? gasConsumption;
  final double? monthlyAmount;
  final bool energyBillConcerns;
  
  // Materials and Interventions
  final double radiatorFoilMeters;
  final bool radiatorFanNeeded;
  final bool smallPowerStripNeeded;
  final bool ledLampsNeeded;
  final int e14LedsCount;
  final int e27LedsCount;
  final double draftStripMeters;
  final bool doorDraftBand;
  final bool doorClosers;
  final bool doorCloserSpring;
  
  // Door Assessment
  final bool allInteriorDoorsPresent;
  final String? missingDoors;
  final String? missingDoorsLivingRoom;
  final String? missingDoorsKitchen;
  final String? missingDoorsBedroom;
  final String? missingDoorsHallway;
  
  // Bathroom Equipment
  final bool showerTimer;
  final bool showerHead;
  
  // Heating System (CV)
  final bool cvWebsiteMentioned;
  final int? currentCvTemperature;
  final int? cvTemperatureLoweredTo;
  final bool cvWaterPressureUnder1Bar;
  final bool tapComfortOff;
  final bool largePowerStripNeeded;
  
  // Problems and Issues
  final String? problemsWith;
  final bool moldIssues;
  final bool moistureIssues;
  final bool draftIssues;
  final String? problemRoomsDescription;
  final bool hygrometerNeeded;
  
  // Community Building
  final String? communityBuilding;
  final bool knowsPotentialFixers;
  final bool wantsToHelp;
  final bool tellNeighbors;
  
  // Additional Information
  final bool oldRefrigerator;
  final bool shareInfoWithHousingCorp;
  final bool keepUpdatedOnResults;
  final String? otherRemarks;
  
  // Contact and Photos
  final String? residentEmail;
  final String? photos;
  final String? photosUrl;
  
  // Complaint flags
  final bool moldComplaint;
  final bool draftComplaint;
  
  // KoboToolbox Integration
  final String? koboSubmissionId;
  final String? koboUuid;
  final DateTime? submissionTime;
  final String? visitData;
  
  // Metadata
  final String status;
  final String? notes;
  final DateTime? createdAt;
  final DateTime? updatedAt;

  const Visit({
    this.id,
    this.volunteerId,
    this.volunteer2Id,
    required this.address,
    required this.visitDate,
    this.startTime,
    this.endTime,
    this.appointmentTime,
    this.residentsCount = 1,
    this.energyMeasuresTaken = false,
    this.whichMeasures,
    this.ventilationChecked = false,
    this.energyUsageChecked = false,
    this.contractDuration,
    this.electricityConsumption,
    this.gasConsumption,
    this.monthlyAmount,
    this.energyBillConcerns = false,
    this.radiatorFoilMeters = 0.0,
    this.radiatorFanNeeded = false,
    this.smallPowerStripNeeded = false,
    this.ledLampsNeeded = false,
    this.e14LedsCount = 0,
    this.e27LedsCount = 0,
    this.draftStripMeters = 0.0,
    this.doorDraftBand = false,
    this.doorClosers = false,
    this.doorCloserSpring = false,
    this.allInteriorDoorsPresent = true,
    this.missingDoors,
    this.missingDoorsLivingRoom,
    this.missingDoorsKitchen,
    this.missingDoorsBedroom,
    this.missingDoorsHallway,
    this.showerTimer = false,
    this.showerHead = false,
    this.cvWebsiteMentioned = false,
    this.currentCvTemperature,
    this.cvTemperatureLoweredTo,
    this.cvWaterPressureUnder1Bar = false,
    this.tapComfortOff = false,
    this.largePowerStripNeeded = false,
    this.problemsWith,
    this.moldIssues = false,
    this.moistureIssues = false,
    this.draftIssues = false,
    this.problemRoomsDescription,
    this.hygrometerNeeded = false,
    this.communityBuilding,
    this.knowsPotentialFixers = false,
    this.wantsToHelp = false,
    this.tellNeighbors = false,
    this.oldRefrigerator = false,
    this.shareInfoWithHousingCorp = false,
    this.keepUpdatedOnResults = false,
    this.otherRemarks,
    this.residentEmail,
    this.photos,
    this.photosUrl,
    this.moldComplaint = false,
    this.draftComplaint = false,
    this.koboSubmissionId,
    this.koboUuid,
    this.submissionTime,
    this.visitData,
    this.status = 'completed',
    this.notes,
    this.createdAt,
    this.updatedAt,
  });

  factory Visit.fromJson(Map<String, dynamic> json) => _$VisitFromJson(json);
  Map<String, dynamic> toJson() => _$VisitToJson(this);

  // Convert from database map
  factory Visit.fromMap(Map<String, dynamic> map) {
    return Visit(
      id: map['id'] as int?,
      volunteerId: map['volunteer_id'] as int?,
      volunteer2Id: map['volunteer_2_id'] as int?,
      address: map['address'] as String,
      visitDate: _parseDateTime(map['visit_date']) ?? DateTime.now(),
      startTime: _parseDateTime(map['start_time']),
      endTime: _parseDateTime(map['end_time']),
      appointmentTime: map['appointment_time'] as String?,
      residentsCount: map['residents_count'] as int? ?? 1,
      energyMeasuresTaken: (map['energy_measures_taken'] as int?) == 1,
      whichMeasures: map['which_measures'] as String?,
      ventilationChecked: (map['ventilation_checked'] as int?) == 1,
      energyUsageChecked: (map['energy_usage_checked'] as int?) == 1,
      contractDuration: map['contract_duration'] as String?,
      electricityConsumption: map['electricity_consumption'] as double?,
      gasConsumption: map['gas_consumption'] as double?,
      monthlyAmount: map['monthly_amount'] as double?,
      energyBillConcerns: (map['energy_bill_concerns'] as int?) == 1,
      radiatorFoilMeters: map['radiator_foil_meters'] as double? ?? 0.0,
      radiatorFanNeeded: (map['radiator_fan_needed'] as int?) == 1,
      smallPowerStripNeeded: (map['small_power_strip_needed'] as int?) == 1,
      ledLampsNeeded: (map['led_lamps_needed'] as int?) == 1,
      e14LedsCount: map['e14_leds_count'] as int? ?? 0,
      e27LedsCount: map['e27_leds_count'] as int? ?? 0,
      draftStripMeters: map['draft_strip_meters'] as double? ?? 0.0,
      doorDraftBand: (map['door_draft_band'] as int?) == 1,
      doorClosers: (map['door_closers'] as int?) == 1,
      doorCloserSpring: (map['door_closer_spring'] as int?) == 1,
      allInteriorDoorsPresent: (map['all_interior_doors_present'] as int?) != 0,
      missingDoors: map['missing_doors'] as String?,
      missingDoorsLivingRoom: map['missing_doors_living_room'] as String?,
      missingDoorsKitchen: map['missing_doors_kitchen'] as String?,
      missingDoorsBedroom: map['missing_doors_bedroom'] as String?,
      missingDoorsHallway: map['missing_doors_hallway'] as String?,
      showerTimer: (map['shower_timer'] as int?) == 1,
      showerHead: (map['shower_head'] as int?) == 1,
      cvWebsiteMentioned: (map['cv_website_mentioned'] as int?) == 1,
      currentCvTemperature: map['current_cv_temperature'] as int?,
      cvTemperatureLoweredTo: map['cv_temperature_lowered_to'] as int?,
      cvWaterPressureUnder1Bar: (map['cv_water_pressure_under_1_bar'] as int?) == 1,
      tapComfortOff: (map['tap_comfort_off'] as int?) == 1,
      largePowerStripNeeded: (map['large_power_strip_needed'] as int?) == 1,
      problemsWith: map['problems_with'] as String?,
      moldIssues: (map['mold_issues'] as int?) == 1,
      moistureIssues: (map['moisture_issues'] as int?) == 1,
      draftIssues: (map['draft_issues'] as int?) == 1,
      problemRoomsDescription: map['problem_rooms_description'] as String?,
      hygrometerNeeded: (map['hygrometer_needed'] as int?) == 1,
      communityBuilding: map['community_building'] as String?,
      knowsPotentialFixers: (map['knows_potential_fixers'] as int?) == 1,
      wantsToHelp: (map['wants_to_help'] as int?) == 1,
      tellNeighbors: (map['tell_neighbors'] as int?) == 1,
      oldRefrigerator: (map['old_refrigerator'] as int?) == 1,
      shareInfoWithHousingCorp: (map['share_info_with_housing_corp'] as int?) == 1,
      keepUpdatedOnResults: (map['keep_updated_on_results'] as int?) == 1,
      otherRemarks: map['other_remarks'] as String?,
      residentEmail: map['resident_email'] as String?,
      photos: map['photos'] as String?,
      photosUrl: map['photos_url'] as String?,
      moldComplaint: (map['mold_complaint'] as int?) == 1,
      draftComplaint: (map['draft_complaint'] as int?) == 1,
      koboSubmissionId: map['kobo_submission_id'] as String?,
      koboUuid: map['kobo_uuid'] as String?,
      submissionTime: _parseDateTime(map['submission_time']),
      visitData: map['visit_data'] as String?,
      status: map['status'] as String? ?? 'completed',
      notes: map['notes'] as String?,
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
      'volunteer_id': volunteerId,
      'volunteer_2_id': volunteer2Id,
      'address': address,
      'visit_date': visitDate.toIso8601String().split('T')[0],
      'start_time': startTime?.toIso8601String(),
      'end_time': endTime?.toIso8601String(),
      'appointment_time': appointmentTime,
      'residents_count': residentsCount,
      'energy_measures_taken': energyMeasuresTaken ? 1 : 0,
      'which_measures': whichMeasures,
      'ventilation_checked': ventilationChecked ? 1 : 0,
      'energy_usage_checked': energyUsageChecked ? 1 : 0,
      'contract_duration': contractDuration,
      'electricity_consumption': electricityConsumption,
      'gas_consumption': gasConsumption,
      'monthly_amount': monthlyAmount,
      'energy_bill_concerns': energyBillConcerns ? 1 : 0,
      'radiator_foil_meters': radiatorFoilMeters,
      'radiator_fan_needed': radiatorFanNeeded ? 1 : 0,
      'small_power_strip_needed': smallPowerStripNeeded ? 1 : 0,
      'led_lamps_needed': ledLampsNeeded ? 1 : 0,
      'e14_leds_count': e14LedsCount,
      'e27_leds_count': e27LedsCount,
      'draft_strip_meters': draftStripMeters,
      'door_draft_band': doorDraftBand ? 1 : 0,
      'door_closers': doorClosers ? 1 : 0,
      'door_closer_spring': doorCloserSpring ? 1 : 0,
      'all_interior_doors_present': allInteriorDoorsPresent ? 1 : 0,
      'missing_doors': missingDoors,
      'missing_doors_living_room': missingDoorsLivingRoom,
      'missing_doors_kitchen': missingDoorsKitchen,
      'missing_doors_bedroom': missingDoorsBedroom,
      'missing_doors_hallway': missingDoorsHallway,
      'shower_timer': showerTimer ? 1 : 0,
      'shower_head': showerHead ? 1 : 0,
      'cv_website_mentioned': cvWebsiteMentioned ? 1 : 0,
      'current_cv_temperature': currentCvTemperature,
      'cv_temperature_lowered_to': cvTemperatureLoweredTo,
      'cv_water_pressure_under_1_bar': cvWaterPressureUnder1Bar ? 1 : 0,
      'tap_comfort_off': tapComfortOff ? 1 : 0,
      'large_power_strip_needed': largePowerStripNeeded ? 1 : 0,
      'problems_with': problemsWith,
      'mold_issues': moldIssues ? 1 : 0,
      'moisture_issues': moistureIssues ? 1 : 0,
      'draft_issues': draftIssues ? 1 : 0,
      'problem_rooms_description': problemRoomsDescription,
      'hygrometer_needed': hygrometerNeeded ? 1 : 0,
      'community_building': communityBuilding,
      'knows_potential_fixers': knowsPotentialFixers ? 1 : 0,
      'wants_to_help': wantsToHelp ? 1 : 0,
      'tell_neighbors': tellNeighbors ? 1 : 0,
      'old_refrigerator': oldRefrigerator ? 1 : 0,
      'share_info_with_housing_corp': shareInfoWithHousingCorp ? 1 : 0,
      'keep_updated_on_results': keepUpdatedOnResults ? 1 : 0,
      'other_remarks': otherRemarks,
      'resident_email': residentEmail,
      'photos': photos,
      'photos_url': photosUrl,
      'mold_complaint': moldComplaint ? 1 : 0,
      'draft_complaint': draftComplaint ? 1 : 0,
      'kobo_submission_id': koboSubmissionId,
      'kobo_uuid': koboUuid,
      'submission_time': submissionTime?.toIso8601String(),
      'visit_data': visitData,
      'status': status,
      'notes': notes,
      'created_at': createdAt?.toIso8601String(),
      'updated_at': updatedAt?.toIso8601String(),
    };
  }

  // Helper methods
  List<String> get issuesList {
    List<String> issues = [];
    if (moldIssues) issues.add('Mold');
    if (moistureIssues) issues.add('Moisture');
    if (draftIssues) issues.add('Draft');
    return issues;
  }

  String get issuesText => issuesList.isEmpty ? 'None' : issuesList.join(', ');

  Visit copyWith({
    int? id,
    int? volunteerId,
    int? volunteer2Id,
    String? address,
    DateTime? visitDate,
    DateTime? startTime,
    DateTime? endTime,
    String? appointmentTime,
    int? residentsCount,
    bool? energyMeasuresTaken,
    String? whichMeasures,
    bool? ventilationChecked,
    String? status,
    String? notes,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return Visit(
      id: id ?? this.id,
      volunteerId: volunteerId ?? this.volunteerId,
      volunteer2Id: volunteer2Id ?? this.volunteer2Id,
      address: address ?? this.address,
      visitDate: visitDate ?? this.visitDate,
      startTime: startTime ?? this.startTime,
      endTime: endTime ?? this.endTime,
      appointmentTime: appointmentTime ?? this.appointmentTime,
      residentsCount: residentsCount ?? this.residentsCount,
      energyMeasuresTaken: energyMeasuresTaken ?? this.energyMeasuresTaken,
      whichMeasures: whichMeasures ?? this.whichMeasures,
      ventilationChecked: ventilationChecked ?? this.ventilationChecked,
      status: status ?? this.status,
      notes: notes ?? this.notes,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      // Include all other fields...
    );
  }

  @override
  String toString() {
    return 'Visit(id: $id, address: $address, visitDate: $visitDate, status: $status)';
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is Visit && other.id == id;
  }

  @override
  int get hashCode => id.hashCode;
}
