// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "BlueprintScreenshotTool/Public/BlueprintScreenshotToolTypes.h"
PRAGMA_DISABLE_DEPRECATION_WARNINGS
void EmptyLinkFunctionForGeneratedCodeBlueprintScreenshotToolTypes() {}

// Begin Cross Module References
BLUEPRINTSCREENSHOTTOOL_API UEnum* Z_Construct_UEnum_BlueprintScreenshotTool_EBSTImageFormat();
BLUEPRINTSCREENSHOTTOOL_API UScriptStruct* Z_Construct_UScriptStruct_FBSTScreenshotData();
COREUOBJECT_API UScriptStruct* Z_Construct_UScriptStruct_FColor();
COREUOBJECT_API UScriptStruct* Z_Construct_UScriptStruct_FIntVector();
UPackage* Z_Construct_UPackage__Script_BlueprintScreenshotTool();
// End Cross Module References

// Begin ScriptStruct FBSTScreenshotData
static FStructRegistrationInfo Z_Registration_Info_UScriptStruct_BSTScreenshotData;
class UScriptStruct* FBSTScreenshotData::StaticStruct()
{
	if (!Z_Registration_Info_UScriptStruct_BSTScreenshotData.OuterSingleton)
	{
		Z_Registration_Info_UScriptStruct_BSTScreenshotData.OuterSingleton = GetStaticStruct(Z_Construct_UScriptStruct_FBSTScreenshotData, (UObject*)Z_Construct_UPackage__Script_BlueprintScreenshotTool(), TEXT("BSTScreenshotData"));
	}
	return Z_Registration_Info_UScriptStruct_BSTScreenshotData.OuterSingleton;
}
template<> BLUEPRINTSCREENSHOTTOOL_API UScriptStruct* StaticStruct<FBSTScreenshotData>()
{
	return FBSTScreenshotData::StaticStruct();
}
struct Z_Construct_UScriptStruct_FBSTScreenshotData_Statics
{
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Struct_MetaDataParams[] = {
		{ "BlueprintType", "true" },
		{ "ModuleRelativePath", "Public/BlueprintScreenshotToolTypes.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_ColorData_MetaData[] = {
		{ "Category", "Screenshot Data" },
		{ "ModuleRelativePath", "Public/BlueprintScreenshotToolTypes.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_Size_MetaData[] = {
		{ "Category", "Screenshot Data" },
		{ "ModuleRelativePath", "Public/BlueprintScreenshotToolTypes.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_CustomName_MetaData[] = {
		{ "Category", "Screenshot Data" },
		{ "ModuleRelativePath", "Public/BlueprintScreenshotToolTypes.h" },
	};
#endif // WITH_METADATA
	static const UECodeGen_Private::FStructPropertyParams NewProp_ColorData_Inner;
	static const UECodeGen_Private::FArrayPropertyParams NewProp_ColorData;
	static const UECodeGen_Private::FStructPropertyParams NewProp_Size;
	static const UECodeGen_Private::FStrPropertyParams NewProp_CustomName;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
	static void* NewStructOps()
	{
		return (UScriptStruct::ICppStructOps*)new UScriptStruct::TCppStructOps<FBSTScreenshotData>();
	}
	static const UECodeGen_Private::FStructParams StructParams;
};
const UECodeGen_Private::FStructPropertyParams Z_Construct_UScriptStruct_FBSTScreenshotData_Statics::NewProp_ColorData_Inner = { "ColorData", nullptr, (EPropertyFlags)0x0000000000000000, UECodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, 0, Z_Construct_UScriptStruct_FColor, METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FArrayPropertyParams Z_Construct_UScriptStruct_FBSTScreenshotData_Statics::NewProp_ColorData = { "ColorData", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Array, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(FBSTScreenshotData, ColorData), EArrayPropertyFlags::None, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_ColorData_MetaData), NewProp_ColorData_MetaData) };
const UECodeGen_Private::FStructPropertyParams Z_Construct_UScriptStruct_FBSTScreenshotData_Statics::NewProp_Size = { "Size", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Struct, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(FBSTScreenshotData, Size), Z_Construct_UScriptStruct_FIntVector, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_Size_MetaData), NewProp_Size_MetaData) };
const UECodeGen_Private::FStrPropertyParams Z_Construct_UScriptStruct_FBSTScreenshotData_Statics::NewProp_CustomName = { "CustomName", nullptr, (EPropertyFlags)0x0010000000000005, UECodeGen_Private::EPropertyGenFlags::Str, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(FBSTScreenshotData, CustomName), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_CustomName_MetaData), NewProp_CustomName_MetaData) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UScriptStruct_FBSTScreenshotData_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FBSTScreenshotData_Statics::NewProp_ColorData_Inner,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FBSTScreenshotData_Statics::NewProp_ColorData,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FBSTScreenshotData_Statics::NewProp_Size,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UScriptStruct_FBSTScreenshotData_Statics::NewProp_CustomName,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FBSTScreenshotData_Statics::PropPointers) < 2048);
const UECodeGen_Private::FStructParams Z_Construct_UScriptStruct_FBSTScreenshotData_Statics::StructParams = {
	(UObject* (*)())Z_Construct_UPackage__Script_BlueprintScreenshotTool,
	nullptr,
	&NewStructOps,
	"BSTScreenshotData",
	Z_Construct_UScriptStruct_FBSTScreenshotData_Statics::PropPointers,
	UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FBSTScreenshotData_Statics::PropPointers),
	sizeof(FBSTScreenshotData),
	alignof(FBSTScreenshotData),
	RF_Public|RF_Transient|RF_MarkAsNative,
	EStructFlags(0x00000201),
	METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UScriptStruct_FBSTScreenshotData_Statics::Struct_MetaDataParams), Z_Construct_UScriptStruct_FBSTScreenshotData_Statics::Struct_MetaDataParams)
};
UScriptStruct* Z_Construct_UScriptStruct_FBSTScreenshotData()
{
	if (!Z_Registration_Info_UScriptStruct_BSTScreenshotData.InnerSingleton)
	{
		UECodeGen_Private::ConstructUScriptStruct(Z_Registration_Info_UScriptStruct_BSTScreenshotData.InnerSingleton, Z_Construct_UScriptStruct_FBSTScreenshotData_Statics::StructParams);
	}
	return Z_Registration_Info_UScriptStruct_BSTScreenshotData.InnerSingleton;
}
// End ScriptStruct FBSTScreenshotData

// Begin Enum EBSTImageFormat
static FEnumRegistrationInfo Z_Registration_Info_UEnum_EBSTImageFormat;
static UEnum* EBSTImageFormat_StaticEnum()
{
	if (!Z_Registration_Info_UEnum_EBSTImageFormat.OuterSingleton)
	{
		Z_Registration_Info_UEnum_EBSTImageFormat.OuterSingleton = GetStaticEnum(Z_Construct_UEnum_BlueprintScreenshotTool_EBSTImageFormat, (UObject*)Z_Construct_UPackage__Script_BlueprintScreenshotTool(), TEXT("EBSTImageFormat"));
	}
	return Z_Registration_Info_UEnum_EBSTImageFormat.OuterSingleton;
}
template<> BLUEPRINTSCREENSHOTTOOL_API UEnum* StaticEnum<EBSTImageFormat>()
{
	return EBSTImageFormat_StaticEnum();
}
struct Z_Construct_UEnum_BlueprintScreenshotTool_EBSTImageFormat_Statics
{
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Enum_MetaDataParams[] = {
		{ "JPG.Name", "EBSTImageFormat::JPG" },
		{ "ModuleRelativePath", "Public/BlueprintScreenshotToolTypes.h" },
		{ "PNG.Name", "EBSTImageFormat::PNG" },
	};
#endif // WITH_METADATA
	static constexpr UECodeGen_Private::FEnumeratorParam Enumerators[] = {
		{ "EBSTImageFormat::PNG", (int64)EBSTImageFormat::PNG },
		{ "EBSTImageFormat::JPG", (int64)EBSTImageFormat::JPG },
	};
	static const UECodeGen_Private::FEnumParams EnumParams;
};
const UECodeGen_Private::FEnumParams Z_Construct_UEnum_BlueprintScreenshotTool_EBSTImageFormat_Statics::EnumParams = {
	(UObject*(*)())Z_Construct_UPackage__Script_BlueprintScreenshotTool,
	nullptr,
	"EBSTImageFormat",
	"EBSTImageFormat",
	Z_Construct_UEnum_BlueprintScreenshotTool_EBSTImageFormat_Statics::Enumerators,
	RF_Public|RF_Transient|RF_MarkAsNative,
	UE_ARRAY_COUNT(Z_Construct_UEnum_BlueprintScreenshotTool_EBSTImageFormat_Statics::Enumerators),
	EEnumFlags::None,
	(uint8)UEnum::ECppForm::EnumClass,
	METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UEnum_BlueprintScreenshotTool_EBSTImageFormat_Statics::Enum_MetaDataParams), Z_Construct_UEnum_BlueprintScreenshotTool_EBSTImageFormat_Statics::Enum_MetaDataParams)
};
UEnum* Z_Construct_UEnum_BlueprintScreenshotTool_EBSTImageFormat()
{
	if (!Z_Registration_Info_UEnum_EBSTImageFormat.InnerSingleton)
	{
		UECodeGen_Private::ConstructUEnum(Z_Registration_Info_UEnum_EBSTImageFormat.InnerSingleton, Z_Construct_UEnum_BlueprintScreenshotTool_EBSTImageFormat_Statics::EnumParams);
	}
	return Z_Registration_Info_UEnum_EBSTImageFormat.InnerSingleton;
}
// End Enum EBSTImageFormat

// Begin Registration
struct Z_CompiledInDeferFile_FID_HostProject_Plugins_BlueprintScreenshotTool_Source_BlueprintScreenshotTool_Public_BlueprintScreenshotToolTypes_h_Statics
{
	static constexpr FEnumRegisterCompiledInInfo EnumInfo[] = {
		{ EBSTImageFormat_StaticEnum, TEXT("EBSTImageFormat"), &Z_Registration_Info_UEnum_EBSTImageFormat, CONSTRUCT_RELOAD_VERSION_INFO(FEnumReloadVersionInfo, 705035250U) },
	};
	static constexpr FStructRegisterCompiledInInfo ScriptStructInfo[] = {
		{ FBSTScreenshotData::StaticStruct, Z_Construct_UScriptStruct_FBSTScreenshotData_Statics::NewStructOps, TEXT("BSTScreenshotData"), &Z_Registration_Info_UScriptStruct_BSTScreenshotData, CONSTRUCT_RELOAD_VERSION_INFO(FStructReloadVersionInfo, sizeof(FBSTScreenshotData), 2575839632U) },
	};
};
static FRegisterCompiledInInfo Z_CompiledInDeferFile_FID_HostProject_Plugins_BlueprintScreenshotTool_Source_BlueprintScreenshotTool_Public_BlueprintScreenshotToolTypes_h_1845400391(TEXT("/Script/BlueprintScreenshotTool"),
	nullptr, 0,
	Z_CompiledInDeferFile_FID_HostProject_Plugins_BlueprintScreenshotTool_Source_BlueprintScreenshotTool_Public_BlueprintScreenshotToolTypes_h_Statics::ScriptStructInfo, UE_ARRAY_COUNT(Z_CompiledInDeferFile_FID_HostProject_Plugins_BlueprintScreenshotTool_Source_BlueprintScreenshotTool_Public_BlueprintScreenshotToolTypes_h_Statics::ScriptStructInfo),
	Z_CompiledInDeferFile_FID_HostProject_Plugins_BlueprintScreenshotTool_Source_BlueprintScreenshotTool_Public_BlueprintScreenshotToolTypes_h_Statics::EnumInfo, UE_ARRAY_COUNT(Z_CompiledInDeferFile_FID_HostProject_Plugins_BlueprintScreenshotTool_Source_BlueprintScreenshotTool_Public_BlueprintScreenshotToolTypes_h_Statics::EnumInfo));
// End Registration
PRAGMA_ENABLE_DEPRECATION_WARNINGS
