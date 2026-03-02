---
id: skill_json_to_dart_model
name: json-to-dart-model
version: 1.0.0
description: Converts JSON data snippets into Flutter/Dart data models with JsonSerializable support.
tags: [flutter, data, code_generation]
permissions: [write_file]
---

# JSON to Dart Model Skill

## Goal
To quickly generate type-safe Dart models from raw JSON responses, ensuring they are compatible with `json_serializable` and `freezed` (if used).

## Instructions
1.  **Input Analysis**:
    *   Review the provided JSON snippet.
    *   Determine the class name (e.g., if JSON is a user object, class is `UserModel`).

2.  **Field Mapping**:
    *   Map JSON types to Dart types:
        *   `string` -> `String`
        *   `number` -> `int` or `double`
        *   `boolean` -> `bool`
        *   `array` -> `List<T>`
        *   `object` -> `AnotherClass`
    *   Detect nullable fields (if context implies).

3.  **Code Generation**:
    *   Create a Dart file with `JsonSerializable` annotations.
    *   Include `factory keys`.
    *   Include `toJson` method.

## Example Output
```dart
import 'package:json_annotation/json_annotation.dart';

part 'user_model.g.dart';

@JsonSerializable()
class UserModel {
  final int id;
  final String name;
  @JsonKey(name: 'email_address')
  final String email;

  UserModel({required this.id, required this.name, required this.email});

  factory UserModel.fromJson(Map<String, dynamic> json) => _$UserModelFromJson(json);
  Map<String, dynamic> toJson() => _$UserModelToJson(this);
}
```
