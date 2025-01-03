// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

// IWYU pragma: private, include "BlueprintAssistSettings.h"
#include "UObject/ObjectMacros.h"
#include "UObject/ScriptMacros.h"

PRAGMA_DISABLE_DEPRECATION_WARNINGS
#ifdef BLUEPRINTASSIST_BlueprintAssistSettings_generated_h
#error "BlueprintAssistSettings.generated.h already included, missing '#pragma once' in BlueprintAssistSettings.h"
#endif
#define BLUEPRINTASSIST_BlueprintAssistSettings_generated_h

#define FID_Build_U5M_Marketplace_Mac_Sync_LocalBuilds_PluginTemp_HostProject_Plugins_BlueprintAssist_Source_BlueprintAssist_Public_BlueprintAssistSettings_h_99_GENERATED_BODY \
	friend struct Z_Construct_UScriptStruct_FBAKnotTrackSettings_Statics; \
	BLUEPRINTASSIST_API static class UScriptStruct* StaticStruct();


template<> BLUEPRINTASSIST_API UScriptStruct* StaticStruct<struct FBAKnotTrackSettings>();

#define FID_Build_U5M_Marketplace_Mac_Sync_LocalBuilds_PluginTemp_HostProject_Plugins_BlueprintAssist_Source_BlueprintAssist_Public_BlueprintAssistSettings_h_113_GENERATED_BODY \
	friend struct Z_Construct_UScriptStruct_FBAFormatterSettings_Statics; \
	BLUEPRINTASSIST_API static class UScriptStruct* StaticStruct();


template<> BLUEPRINTASSIST_API UScriptStruct* StaticStruct<struct FBAFormatterSettings>();

#define FID_Build_U5M_Marketplace_Mac_Sync_LocalBuilds_PluginTemp_HostProject_Plugins_BlueprintAssist_Source_BlueprintAssist_Public_BlueprintAssistSettings_h_164_INCLASS_NO_PURE_DECLS \
private: \
	static void StaticRegisterNativesUBASettings(); \
	friend struct Z_Construct_UClass_UBASettings_Statics; \
public: \
	DECLARE_CLASS(UBASettings, UObject, COMPILED_IN_FLAGS(0 | CLASS_Config), CASTCLASS_None, TEXT("/Script/BlueprintAssist"), NO_API) \
	DECLARE_SERIALIZER(UBASettings) \
	static const TCHAR* StaticConfigName() {return TEXT("EditorPerProjectUserSettings");} \



#define FID_Build_U5M_Marketplace_Mac_Sync_LocalBuilds_PluginTemp_HostProject_Plugins_BlueprintAssist_Source_BlueprintAssist_Public_BlueprintAssistSettings_h_164_ENHANCED_CONSTRUCTORS \
private: \
	/** Private move- and copy-constructors, should never be used */ \
	UBASettings(UBASettings&&); \
	UBASettings(const UBASettings&); \
public: \
	DECLARE_VTABLE_PTR_HELPER_CTOR(NO_API, UBASettings); \
	DEFINE_VTABLE_PTR_HELPER_CTOR_CALLER(UBASettings); \
	DEFINE_DEFAULT_OBJECT_INITIALIZER_CONSTRUCTOR_CALL(UBASettings) \
	NO_API virtual ~UBASettings();


#define FID_Build_U5M_Marketplace_Mac_Sync_LocalBuilds_PluginTemp_HostProject_Plugins_BlueprintAssist_Source_BlueprintAssist_Public_BlueprintAssistSettings_h_161_PROLOG
#define FID_Build_U5M_Marketplace_Mac_Sync_LocalBuilds_PluginTemp_HostProject_Plugins_BlueprintAssist_Source_BlueprintAssist_Public_BlueprintAssistSettings_h_164_GENERATED_BODY \
PRAGMA_DISABLE_DEPRECATION_WARNINGS \
public: \
	FID_Build_U5M_Marketplace_Mac_Sync_LocalBuilds_PluginTemp_HostProject_Plugins_BlueprintAssist_Source_BlueprintAssist_Public_BlueprintAssistSettings_h_164_INCLASS_NO_PURE_DECLS \
	FID_Build_U5M_Marketplace_Mac_Sync_LocalBuilds_PluginTemp_HostProject_Plugins_BlueprintAssist_Source_BlueprintAssist_Public_BlueprintAssistSettings_h_164_ENHANCED_CONSTRUCTORS \
private: \
PRAGMA_ENABLE_DEPRECATION_WARNINGS


template<> BLUEPRINTASSIST_API UClass* StaticClass<class UBASettings>();

#undef CURRENT_FILE_ID
#define CURRENT_FILE_ID FID_Build_U5M_Marketplace_Mac_Sync_LocalBuilds_PluginTemp_HostProject_Plugins_BlueprintAssist_Source_BlueprintAssist_Public_BlueprintAssistSettings_h


#define FOREACH_ENUM_EBACACHESAVELOCATION(op) \
	op(EBACacheSaveLocation::Plugin) \
	op(EBACacheSaveLocation::Project) 

enum class EBACacheSaveLocation : uint8;
template<> struct TIsUEnumClass<EBACacheSaveLocation> { enum { Value = true }; };
template<> BLUEPRINTASSIST_API UEnum* StaticEnum<EBACacheSaveLocation>();

#define FOREACH_ENUM_EBANODEFORMATTINGSTYLE(op) \
	op(EBANodeFormattingStyle::Expanded) \
	op(EBANodeFormattingStyle::Compact) 

enum class EBANodeFormattingStyle : uint8;
template<> struct TIsUEnumClass<EBANodeFormattingStyle> { enum { Value = true }; };
template<> BLUEPRINTASSIST_API UEnum* StaticEnum<EBANodeFormattingStyle>();

#define FOREACH_ENUM_EBAPARAMETERFORMATTINGSTYLE(op) \
	op(EBAParameterFormattingStyle::Helixing) \
	op(EBAParameterFormattingStyle::LeftSide) 

enum class EBAParameterFormattingStyle : uint8;
template<> struct TIsUEnumClass<EBAParameterFormattingStyle> { enum { Value = true }; };
template<> BLUEPRINTASSIST_API UEnum* StaticEnum<EBAParameterFormattingStyle>();

#define FOREACH_ENUM_EBAWIRINGSTYLE(op) \
	op(EBAWiringStyle::AlwaysMerge) \
	op(EBAWiringStyle::MergeWhenNear) \
	op(EBAWiringStyle::SingleWire) 

enum class EBAWiringStyle : uint8;
template<> struct TIsUEnumClass<EBAWiringStyle> { enum { Value = true }; };
template<> BLUEPRINTASSIST_API UEnum* StaticEnum<EBAWiringStyle>();

#define FOREACH_ENUM_EBAAUTOFORMATTING(op) \
	op(EBAAutoFormatting::Never) \
	op(EBAAutoFormatting::FormatAllConnected) \
	op(EBAAutoFormatting::FormatSingleConnected) 

enum class EBAAutoFormatting : uint8;
template<> struct TIsUEnumClass<EBAAutoFormatting> { enum { Value = true }; };
template<> BLUEPRINTASSIST_API UEnum* StaticEnum<EBAAutoFormatting>();

#define FOREACH_ENUM_EBAFORMATALLSTYLE(op) \
	op(EBAFormatAllStyle::Simple) \
	op(EBAFormatAllStyle::Smart) \
	op(EBAFormatAllStyle::NodeType) 

enum class EBAFormatAllStyle : uint8;
template<> struct TIsUEnumClass<EBAFormatAllStyle> { enum { Value = true }; };
template<> BLUEPRINTASSIST_API UEnum* StaticEnum<EBAFormatAllStyle>();

#define FOREACH_ENUM_EBAFORMATALLHORIZONTALALIGNMENT(op) \
	op(EBAFormatAllHorizontalAlignment::RootNode) \
	op(EBAFormatAllHorizontalAlignment::Comment) 

enum class EBAFormatAllHorizontalAlignment : uint8;
template<> struct TIsUEnumClass<EBAFormatAllHorizontalAlignment> { enum { Value = true }; };
template<> BLUEPRINTASSIST_API UEnum* StaticEnum<EBAFormatAllHorizontalAlignment>();

#define FOREACH_ENUM_EBAFORMATTERTYPE(op) \
	op(EBAFormatterType::Blueprint) \
	op(EBAFormatterType::BehaviorTree) \
	op(EBAFormatterType::Simple) 

enum class EBAFormatterType : uint8;
template<> struct TIsUEnumClass<EBAFormatterType> { enum { Value = true }; };
template<> BLUEPRINTASSIST_API UEnum* StaticEnum<EBAFormatterType>();

#define FOREACH_ENUM_EBAAUTOZOOMTONODE(op) \
	op(EBAAutoZoomToNode::Never) \
	op(EBAAutoZoomToNode::Always) \
	op(EBAAutoZoomToNode::Outside_Viewport) 

enum class EBAAutoZoomToNode : uint8;
template<> struct TIsUEnumClass<EBAAutoZoomToNode> { enum { Value = true }; };
template<> BLUEPRINTASSIST_API UEnum* StaticEnum<EBAAutoZoomToNode>();

#define FOREACH_ENUM_EBAFUNCTIONACCESSSPECIFIER(op) \
	op(EBAFunctionAccessSpecifier::Public) \
	op(EBAFunctionAccessSpecifier::Protected) \
	op(EBAFunctionAccessSpecifier::Private) 

enum class EBAFunctionAccessSpecifier : uint8;
template<> struct TIsUEnumClass<EBAFunctionAccessSpecifier> { enum { Value = true }; };
template<> BLUEPRINTASSIST_API UEnum* StaticEnum<EBAFunctionAccessSpecifier>();

PRAGMA_ENABLE_DEPRECATION_WARNINGS
