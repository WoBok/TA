// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "BlueprintScreenshotTool/Public/BlueprintScreenshotToolSettings.h"
#include "Runtime/Slate/Public/Framework/Commands/InputChord.h"
PRAGMA_DISABLE_DEPRECATION_WARNINGS
void EmptyLinkFunctionForGeneratedCodeBlueprintScreenshotToolSettings() {}

// Begin Cross Module References
BLUEPRINTSCREENSHOTTOOL_API UClass* Z_Construct_UClass_UBlueprintScreenshotToolSettings();
BLUEPRINTSCREENSHOTTOOL_API UClass* Z_Construct_UClass_UBlueprintScreenshotToolSettings_NoRegister();
BLUEPRINTSCREENSHOTTOOL_API UEnum* Z_Construct_UEnum_BlueprintScreenshotTool_EBSTImageFormat();
COREUOBJECT_API UClass* Z_Construct_UClass_UObject();
COREUOBJECT_API UScriptStruct* Z_Construct_UScriptStruct_FDirectoryPath();
SLATE_API UScriptStruct* Z_Construct_UScriptStruct_FInputChord();
UPackage* Z_Construct_UPackage__Script_BlueprintScreenshotTool();
// End Cross Module References

// Begin Class UBlueprintScreenshotToolSettings
void UBlueprintScreenshotToolSettings::StaticRegisterNativesUBlueprintScreenshotToolSettings()
{
}
IMPLEMENT_CLASS_NO_AUTO_REGISTRATION(UBlueprintScreenshotToolSettings);
UClass* Z_Construct_UClass_UBlueprintScreenshotToolSettings_NoRegister()
{
	return UBlueprintScreenshotToolSettings::StaticClass();
}
struct Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics
{
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Class_MetaDataParams[] = {
		{ "BlueprintType", "true" },
		{ "IncludePath", "BlueprintScreenshotToolSettings.h" },
		{ "ModuleRelativePath", "Public/BlueprintScreenshotToolSettings.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bOverrideScreenshotNaming_MetaData[] = {
		{ "Category", "BlueprintScreenshotTool|General" },
		{ "Comment", "// If enabled the screenshot will be saved with the custom name\n" },
		{ "InlineEditConditionToggle", "" },
		{ "ModuleRelativePath", "Public/BlueprintScreenshotToolSettings.h" },
		{ "ToolTip", "If enabled the screenshot will be saved with the custom name" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_ScreenshotBaseName_MetaData[] = {
		{ "Category", "BlueprintScreenshotTool|General" },
		{ "Comment", "// Will be used as a base name for the screenshot, instead of format <AssetName>_<GraphName>\n" },
		{ "EditCondition", "bOverrideScreenshotNaming" },
		{ "ModuleRelativePath", "Public/BlueprintScreenshotToolSettings.h" },
		{ "ToolTip", "Will be used as a base name for the screenshot, instead of format <AssetName>_<GraphName>" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_Extension_MetaData[] = {
		{ "Category", "BlueprintScreenshotTool|General" },
		{ "Comment", "// Screenshot file format\n" },
		{ "ModuleRelativePath", "Public/BlueprintScreenshotToolSettings.h" },
		{ "ToolTip", "Screenshot file format" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_Quality_MetaData[] = {
		{ "Category", "BlueprintScreenshotTool|General" },
		{ "ClampMax", "100" },
		{ "ClampMin", "10" },
		{ "Comment", "// Quality of jpg image. 10-100\n" },
		{ "EditCondition", "Extension == EBSTImageFormat::JPG" },
		{ "ModuleRelativePath", "Public/BlueprintScreenshotToolSettings.h" },
		{ "ToolTip", "Quality of jpg image. 10-100" },
		{ "UIMax", "100" },
		{ "UIMin", "10" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_SaveDirectory_MetaData[] = {
		{ "Category", "BlueprintScreenshotTool|General" },
		{ "Comment", "// Directory where the screenshots will be saved\n" },
		{ "ModuleRelativePath", "Public/BlueprintScreenshotToolSettings.h" },
		{ "RelativePath", "" },
		{ "ToolTip", "Directory where the screenshots will be saved" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_ScreenshotPadding_MetaData[] = {
		{ "Category", "BlueprintScreenshotTool|General" },
		{ "Comment", "// Padding around selected graph nodes in pixels when taking screenshot\n" },
		{ "ModuleRelativePath", "Public/BlueprintScreenshotToolSettings.h" },
		{ "ToolTip", "Padding around selected graph nodes in pixels when taking screenshot" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_MinScreenshotSize_MetaData[] = {
		{ "Category", "BlueprintScreenshotTool|General" },
		{ "Comment", "// Minimum screenshot size in pixels\n" },
		{ "ModuleRelativePath", "Public/BlueprintScreenshotToolSettings.h" },
		{ "ToolTip", "Minimum screenshot size in pixels" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_MaxScreenshotSize_MetaData[] = {
		{ "Category", "BlueprintScreenshotTool|General" },
		{ "Comment", "// Maximum screenshot size in pixels\n" },
		{ "ModuleRelativePath", "Public/BlueprintScreenshotToolSettings.h" },
		{ "ToolTip", "Maximum screenshot size in pixels" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_ZoomAmount_MetaData[] = {
		{ "Category", "BlueprintScreenshotTool|General" },
		{ "ClampMax", "2" },
		{ "ClampMin", "0.1" },
		{ "Comment", "// Default zoom amount that is used when taking screenshot of selected nodes. ATTENTION: It will scale the size of the screenshot as well. This operation can be slow.\n" },
		{ "ModuleRelativePath", "Public/BlueprintScreenshotToolSettings.h" },
		{ "ToolTip", "Default zoom amount that is used when taking screenshot of selected nodes. ATTENTION: It will scale the size of the screenshot as well. This operation can be slow." },
		{ "UIMax", "2" },
		{ "UIMin", "0.1" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_TakeScreenshotHotkey_MetaData[] = {
		{ "Category", "BlueprintScreenshotTool|Hotkeys" },
		{ "ConfigRestartRequired", "TRUE" },
		{ "ModuleRelativePath", "Public/BlueprintScreenshotToolSettings.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_OpenDirectoryHotkey_MetaData[] = {
		{ "Category", "BlueprintScreenshotTool|Hotkeys" },
		{ "ConfigRestartRequired", "TRUE" },
		{ "ModuleRelativePath", "Public/BlueprintScreenshotToolSettings.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bShowNotification_MetaData[] = {
		{ "Category", "BlueprintScreenshotTool|Notification" },
		{ "Comment", "// If true, the notification with hyperlink to the screenshot will be shown after taking the screenshot\n" },
		{ "ModuleRelativePath", "Public/BlueprintScreenshotToolSettings.h" },
		{ "ToolTip", "If true, the notification with hyperlink to the screenshot will be shown after taking the screenshot" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_NotificationMessageFormat_MetaData[] = {
		{ "Category", "BlueprintScreenshotTool|DeveloperMode|Notification" },
		{ "EditCondition", "bDeveloperMode" },
		{ "ModuleRelativePath", "Public/BlueprintScreenshotToolSettings.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_ExpireDuration_MetaData[] = {
		{ "Category", "BlueprintScreenshotTool|Notification" },
		{ "Comment", "// How long the notification will be shown in seconds\n" },
		{ "ModuleRelativePath", "Public/BlueprintScreenshotToolSettings.h" },
		{ "ToolTip", "How long the notification will be shown in seconds" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bUseSuccessFailIcons_MetaData[] = {
		{ "Category", "BlueprintScreenshotTool|DeveloperMode|Notification" },
		{ "Comment", "// If true, the notification will use success/fail icons instead of the default info icon\n" },
		{ "EditCondition", "bDeveloperMode" },
		{ "ModuleRelativePath", "Public/BlueprintScreenshotToolSettings.h" },
		{ "ToolTip", "If true, the notification will use success/fail icons instead of the default info icon" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bDeveloperMode_MetaData[] = {
		{ "Category", "BlueprintScreenshotTool|DeveloperMode" },
		{ "ModuleRelativePath", "Public/BlueprintScreenshotToolSettings.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_DiffToolbarTexts_MetaData[] = {
		{ "Category", "BlueprintScreenshotTool|DeveloperMode" },
		{ "Comment", "// The text is used for searching Blueprint Diff toolbar buttons to inject \"Take Screenshot\" button\n" },
		{ "EditCondition", "bDeveloperMode" },
		{ "ModuleRelativePath", "Public/BlueprintScreenshotToolSettings.h" },
		{ "ToolTip", "The text is used for searching Blueprint Diff toolbar buttons to inject \"Take Screenshot\" button" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_DiffWindowButtonLabel_MetaData[] = {
		{ "Category", "BlueprintScreenshotTool|DeveloperMode" },
		{ "EditCondition", "bDeveloperMode" },
		{ "ModuleRelativePath", "Public/BlueprintScreenshotToolSettings.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_DiffWindowButtonToolTip_MetaData[] = {
		{ "Category", "BlueprintScreenshotTool|DeveloperMode" },
		{ "EditCondition", "bDeveloperMode" },
		{ "ModuleRelativePath", "Public/BlueprintScreenshotToolSettings.h" },
	};
#endif // WITH_METADATA
	static void NewProp_bOverrideScreenshotNaming_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bOverrideScreenshotNaming;
	static const UECodeGen_Private::FStrPropertyParams NewProp_ScreenshotBaseName;
	static const UECodeGen_Private::FBytePropertyParams NewProp_Extension_Underlying;
	static const UECodeGen_Private::FEnumPropertyParams NewProp_Extension;
	static const UECodeGen_Private::FIntPropertyParams NewProp_Quality;
	static const UECodeGen_Private::FStructPropertyParams NewProp_SaveDirectory;
	static const UECodeGen_Private::FIntPropertyParams NewProp_ScreenshotPadding;
	static const UECodeGen_Private::FIntPropertyParams NewProp_MinScreenshotSize;
	static const UECodeGen_Private::FIntPropertyParams NewProp_MaxScreenshotSize;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_ZoomAmount;
	static const UECodeGen_Private::FStructPropertyParams NewProp_TakeScreenshotHotkey;
	static const UECodeGen_Private::FStructPropertyParams NewProp_OpenDirectoryHotkey;
	static void NewProp_bShowNotification_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bShowNotification;
	static const UECodeGen_Private::FTextPropertyParams NewProp_NotificationMessageFormat;
	static const UECodeGen_Private::FFloatPropertyParams NewProp_ExpireDuration;
	static void NewProp_bUseSuccessFailIcons_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bUseSuccessFailIcons;
	static void NewProp_bDeveloperMode_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bDeveloperMode;
	static const UECodeGen_Private::FTextPropertyParams NewProp_DiffToolbarTexts_Inner;
	static const UECodeGen_Private::FArrayPropertyParams NewProp_DiffToolbarTexts;
	static const UECodeGen_Private::FTextPropertyParams NewProp_DiffWindowButtonLabel;
	static const UECodeGen_Private::FTextPropertyParams NewProp_DiffWindowButtonToolTip;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
	static UObject* (*const DependentSingletons[])();
	static constexpr FCppClassTypeInfoStatic StaticCppClassTypeInfo = {
		TCppClassTypeTraits<UBlueprintScreenshotToolSettings>::IsAbstract,
	};
	static const UECodeGen_Private::FClassParams ClassParams;
};
void Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_bOverrideScreenshotNaming_SetBit(void* Obj)
{
	((UBlueprintScreenshotToolSettings*)Obj)->bOverrideScreenshotNaming = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_bOverrideScreenshotNaming = { "bOverrideScreenshotNaming", nullptr, (EPropertyFlags)0x0010000000004015, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(UBlueprintScreenshotToolSettings), &Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_bOverrideScreenshotNaming_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bOverrideScreenshotNaming_MetaData), NewProp_bOverrideScreenshotNaming_MetaData) };
const UECodeGen_Private::FStrPropertyParams Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_ScreenshotBaseName = { "ScreenshotBaseName", nullptr, (EPropertyFlags)0x0010000000004015, UECodeGen_Private::EPropertyGenFlags::Str, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBlueprintScreenshotToolSettings, ScreenshotBaseName), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_ScreenshotBaseName_MetaData), NewProp_ScreenshotBaseName_MetaData) };
const UECodeGen_Private::FBytePropertyParams Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_Extension_Underlying = { "UnderlyingType", nullptr, (EPropertyFlags)0x0000000000000000, UECodeGen_Private::EPropertyGenFlags::Byte, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, 0, nullptr, METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FEnumPropertyParams Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_Extension = { "Extension", nullptr, (EPropertyFlags)0x0010000000004015, UECodeGen_Private::EPropertyGenFlags::Enum, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBlueprintScreenshotToolSettings, Extension), Z_Construct_UEnum_BlueprintScreenshotTool_EBSTImageFormat, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_Extension_MetaData), NewProp_Extension_MetaData) }; // 705035250
const UECodeGen_Private::FIntPropertyParams Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_Quality = { "Quality", nullptr, (EPropertyFlags)0x0010000000004015, UECodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBlueprintScreenshotToolSettings, Quality), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_Quality_MetaData), NewProp_Quality_MetaData) };
const UECodeGen_Private::FStructPropertyParams Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_SaveDirectory = { "SaveDirectory", nullptr, (EPropertyFlags)0x0010000000004015, UECodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBlueprintScreenshotToolSettings, SaveDirectory), Z_Construct_UScriptStruct_FDirectoryPath, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_SaveDirectory_MetaData), NewProp_SaveDirectory_MetaData) };
const UECodeGen_Private::FIntPropertyParams Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_ScreenshotPadding = { "ScreenshotPadding", nullptr, (EPropertyFlags)0x0010000000004015, UECodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBlueprintScreenshotToolSettings, ScreenshotPadding), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_ScreenshotPadding_MetaData), NewProp_ScreenshotPadding_MetaData) };
const UECodeGen_Private::FIntPropertyParams Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_MinScreenshotSize = { "MinScreenshotSize", nullptr, (EPropertyFlags)0x0010000000004015, UECodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBlueprintScreenshotToolSettings, MinScreenshotSize), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_MinScreenshotSize_MetaData), NewProp_MinScreenshotSize_MetaData) };
const UECodeGen_Private::FIntPropertyParams Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_MaxScreenshotSize = { "MaxScreenshotSize", nullptr, (EPropertyFlags)0x0010000000004015, UECodeGen_Private::EPropertyGenFlags::Int, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBlueprintScreenshotToolSettings, MaxScreenshotSize), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_MaxScreenshotSize_MetaData), NewProp_MaxScreenshotSize_MetaData) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_ZoomAmount = { "ZoomAmount", nullptr, (EPropertyFlags)0x0010000000004015, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBlueprintScreenshotToolSettings, ZoomAmount), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_ZoomAmount_MetaData), NewProp_ZoomAmount_MetaData) };
const UECodeGen_Private::FStructPropertyParams Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_TakeScreenshotHotkey = { "TakeScreenshotHotkey", nullptr, (EPropertyFlags)0x0010000000004015, UECodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBlueprintScreenshotToolSettings, TakeScreenshotHotkey), Z_Construct_UScriptStruct_FInputChord, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_TakeScreenshotHotkey_MetaData), NewProp_TakeScreenshotHotkey_MetaData) }; // 4109060215
const UECodeGen_Private::FStructPropertyParams Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_OpenDirectoryHotkey = { "OpenDirectoryHotkey", nullptr, (EPropertyFlags)0x0010000000004015, UECodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBlueprintScreenshotToolSettings, OpenDirectoryHotkey), Z_Construct_UScriptStruct_FInputChord, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_OpenDirectoryHotkey_MetaData), NewProp_OpenDirectoryHotkey_MetaData) }; // 4109060215
void Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_bShowNotification_SetBit(void* Obj)
{
	((UBlueprintScreenshotToolSettings*)Obj)->bShowNotification = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_bShowNotification = { "bShowNotification", nullptr, (EPropertyFlags)0x0010000000004015, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(UBlueprintScreenshotToolSettings), &Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_bShowNotification_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bShowNotification_MetaData), NewProp_bShowNotification_MetaData) };
const UECodeGen_Private::FTextPropertyParams Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_NotificationMessageFormat = { "NotificationMessageFormat", nullptr, (EPropertyFlags)0x0010000000004015, UECodeGen_Private::EPropertyGenFlags::Text, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBlueprintScreenshotToolSettings, NotificationMessageFormat), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_NotificationMessageFormat_MetaData), NewProp_NotificationMessageFormat_MetaData) };
const UECodeGen_Private::FFloatPropertyParams Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_ExpireDuration = { "ExpireDuration", nullptr, (EPropertyFlags)0x0010000000004015, UECodeGen_Private::EPropertyGenFlags::Float, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBlueprintScreenshotToolSettings, ExpireDuration), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_ExpireDuration_MetaData), NewProp_ExpireDuration_MetaData) };
void Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_bUseSuccessFailIcons_SetBit(void* Obj)
{
	((UBlueprintScreenshotToolSettings*)Obj)->bUseSuccessFailIcons = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_bUseSuccessFailIcons = { "bUseSuccessFailIcons", nullptr, (EPropertyFlags)0x0010000000004015, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(UBlueprintScreenshotToolSettings), &Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_bUseSuccessFailIcons_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bUseSuccessFailIcons_MetaData), NewProp_bUseSuccessFailIcons_MetaData) };
void Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_bDeveloperMode_SetBit(void* Obj)
{
	((UBlueprintScreenshotToolSettings*)Obj)->bDeveloperMode = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_bDeveloperMode = { "bDeveloperMode", nullptr, (EPropertyFlags)0x0010000000004015, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(UBlueprintScreenshotToolSettings), &Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_bDeveloperMode_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bDeveloperMode_MetaData), NewProp_bDeveloperMode_MetaData) };
const UECodeGen_Private::FTextPropertyParams Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_DiffToolbarTexts_Inner = { "DiffToolbarTexts", nullptr, (EPropertyFlags)0x0000000000004000, UECodeGen_Private::EPropertyGenFlags::Text, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, 0, METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FArrayPropertyParams Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_DiffToolbarTexts = { "DiffToolbarTexts", nullptr, (EPropertyFlags)0x0010000000004015, UECodeGen_Private::EPropertyGenFlags::Array, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBlueprintScreenshotToolSettings, DiffToolbarTexts), EArrayPropertyFlags::None, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_DiffToolbarTexts_MetaData), NewProp_DiffToolbarTexts_MetaData) };
const UECodeGen_Private::FTextPropertyParams Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_DiffWindowButtonLabel = { "DiffWindowButtonLabel", nullptr, (EPropertyFlags)0x0010000000004015, UECodeGen_Private::EPropertyGenFlags::Text, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBlueprintScreenshotToolSettings, DiffWindowButtonLabel), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_DiffWindowButtonLabel_MetaData), NewProp_DiffWindowButtonLabel_MetaData) };
const UECodeGen_Private::FTextPropertyParams Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_DiffWindowButtonToolTip = { "DiffWindowButtonToolTip", nullptr, (EPropertyFlags)0x0010000000004015, UECodeGen_Private::EPropertyGenFlags::Text, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBlueprintScreenshotToolSettings, DiffWindowButtonToolTip), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_DiffWindowButtonToolTip_MetaData), NewProp_DiffWindowButtonToolTip_MetaData) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_bOverrideScreenshotNaming,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_ScreenshotBaseName,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_Extension_Underlying,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_Extension,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_Quality,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_SaveDirectory,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_ScreenshotPadding,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_MinScreenshotSize,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_MaxScreenshotSize,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_ZoomAmount,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_TakeScreenshotHotkey,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_OpenDirectoryHotkey,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_bShowNotification,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_NotificationMessageFormat,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_ExpireDuration,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_bUseSuccessFailIcons,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_bDeveloperMode,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_DiffToolbarTexts_Inner,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_DiffToolbarTexts,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_DiffWindowButtonLabel,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::NewProp_DiffWindowButtonToolTip,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::PropPointers) < 2048);
UObject* (*const Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::DependentSingletons[])() = {
	(UObject* (*)())Z_Construct_UClass_UObject,
	(UObject* (*)())Z_Construct_UPackage__Script_BlueprintScreenshotTool,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::DependentSingletons) < 16);
const UECodeGen_Private::FClassParams Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::ClassParams = {
	&UBlueprintScreenshotToolSettings::StaticClass,
	"BluerpintScreenshotTool",
	&StaticCppClassTypeInfo,
	DependentSingletons,
	nullptr,
	Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::PropPointers,
	nullptr,
	UE_ARRAY_COUNT(DependentSingletons),
	0,
	UE_ARRAY_COUNT(Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::PropPointers),
	0,
	0x001000A4u,
	METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::Class_MetaDataParams), Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::Class_MetaDataParams)
};
UClass* Z_Construct_UClass_UBlueprintScreenshotToolSettings()
{
	if (!Z_Registration_Info_UClass_UBlueprintScreenshotToolSettings.OuterSingleton)
	{
		UECodeGen_Private::ConstructUClass(Z_Registration_Info_UClass_UBlueprintScreenshotToolSettings.OuterSingleton, Z_Construct_UClass_UBlueprintScreenshotToolSettings_Statics::ClassParams);
	}
	return Z_Registration_Info_UClass_UBlueprintScreenshotToolSettings.OuterSingleton;
}
template<> BLUEPRINTSCREENSHOTTOOL_API UClass* StaticClass<UBlueprintScreenshotToolSettings>()
{
	return UBlueprintScreenshotToolSettings::StaticClass();
}
UBlueprintScreenshotToolSettings::UBlueprintScreenshotToolSettings(const FObjectInitializer& ObjectInitializer) : Super(ObjectInitializer) {}
DEFINE_VTABLE_PTR_HELPER_CTOR(UBlueprintScreenshotToolSettings);
UBlueprintScreenshotToolSettings::~UBlueprintScreenshotToolSettings() {}
// End Class UBlueprintScreenshotToolSettings

// Begin Registration
struct Z_CompiledInDeferFile_FID_HostProject_Plugins_BlueprintScreenshotTool_Source_BlueprintScreenshotTool_Public_BlueprintScreenshotToolSettings_h_Statics
{
	static constexpr FClassRegisterCompiledInInfo ClassInfo[] = {
		{ Z_Construct_UClass_UBlueprintScreenshotToolSettings, UBlueprintScreenshotToolSettings::StaticClass, TEXT("UBlueprintScreenshotToolSettings"), &Z_Registration_Info_UClass_UBlueprintScreenshotToolSettings, CONSTRUCT_RELOAD_VERSION_INFO(FClassReloadVersionInfo, sizeof(UBlueprintScreenshotToolSettings), 3145856461U) },
	};
};
static FRegisterCompiledInInfo Z_CompiledInDeferFile_FID_HostProject_Plugins_BlueprintScreenshotTool_Source_BlueprintScreenshotTool_Public_BlueprintScreenshotToolSettings_h_592552957(TEXT("/Script/BlueprintScreenshotTool"),
	Z_CompiledInDeferFile_FID_HostProject_Plugins_BlueprintScreenshotTool_Source_BlueprintScreenshotTool_Public_BlueprintScreenshotToolSettings_h_Statics::ClassInfo, UE_ARRAY_COUNT(Z_CompiledInDeferFile_FID_HostProject_Plugins_BlueprintScreenshotTool_Source_BlueprintScreenshotTool_Public_BlueprintScreenshotToolSettings_h_Statics::ClassInfo),
	nullptr, 0,
	nullptr, 0);
// End Registration
PRAGMA_ENABLE_DEPRECATION_WARNINGS
