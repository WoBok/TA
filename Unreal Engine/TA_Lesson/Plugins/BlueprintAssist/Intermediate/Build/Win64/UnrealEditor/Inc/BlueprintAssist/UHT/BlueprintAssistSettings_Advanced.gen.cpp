// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "BlueprintAssist/Public/BlueprintAssistSettings_Advanced.h"
PRAGMA_DISABLE_DEPRECATION_WARNINGS
void EmptyLinkFunctionForGeneratedCodeBlueprintAssistSettings_Advanced() {}

// Begin Cross Module References
BLUEPRINTASSIST_API UClass* Z_Construct_UClass_UBASettings_Advanced();
BLUEPRINTASSIST_API UClass* Z_Construct_UClass_UBASettings_Advanced_NoRegister();
COREUOBJECT_API UClass* Z_Construct_UClass_UObject();
UPackage* Z_Construct_UPackage__Script_BlueprintAssist();
// End Cross Module References

// Begin Class UBASettings_Advanced
void UBASettings_Advanced::StaticRegisterNativesUBASettings_Advanced()
{
}
IMPLEMENT_CLASS_NO_AUTO_REGISTRATION(UBASettings_Advanced);
UClass* Z_Construct_UClass_UBASettings_Advanced_NoRegister()
{
	return UBASettings_Advanced::StaticClass();
}
struct Z_Construct_UClass_UBASettings_Advanced_Statics
{
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Class_MetaDataParams[] = {
		{ "IncludePath", "BlueprintAssistSettings_Advanced.h" },
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_Advanced.h" },
		{ "ObjectInitializerConstructorDeclared", "" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bRemoveLoopingCausedBySwapping_MetaData[] = {
		{ "Category", "Commands|Swap Nodes" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "/* If swapping produced any looping wires, remove them */" },
#endif
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_Advanced.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "If swapping produced any looping wires, remove them" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_DisabledCommands_MetaData[] = {
		{ "Category", "Commands" },
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_Advanced.h" },
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bEnableMaterialGraphPinHoverFix_MetaData[] = {
		{ "Category", "Material Graph|Experimental" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "/* Potential issue where pins can get stuck in a hovered state on the material graph */" },
#endif
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_Advanced.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Potential issue where pins can get stuck in a hovered state on the material graph" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bGenerateUniqueGUIDForMaterialExpressions_MetaData[] = {
		{ "Category", "Material Graph|Experimental" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "/* Fix for issue where copy-pasting material nodes will result in their material expressions having the same GUID */" },
#endif
		{ "DisplayName", "Generate Unique GUID For Material Expressions" },
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_Advanced.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Fix for issue where copy-pasting material nodes will result in their material expressions having the same GUID" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bStoreCacheDataInPackageMetaData_MetaData[] = {
		{ "Category", "Cache|Experimental" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "/* Instead of making a json file to store cache data, store it in the blueprint's package meta data */" },
#endif
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_Advanced.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Instead of making a json file to store cache data, store it in the blueprint's package meta data" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bPrettyPrintCacheJSON_MetaData[] = {
		{ "Category", "Cache" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "/* Save cache file JSON in a more human-readable format. Useful for debugging, but increases size of cache files.  */" },
#endif
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_Advanced.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Save cache file JSON in a more human-readable format. Useful for debugging, but increases size of cache files." },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bUseCustomBlueprintActionMenu_MetaData[] = {
		{ "Category", "Misc|Experimental" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "/* Use a custom blueprint action menu for creating nodes (very prototype, not supported in 5.0 or earlier) */" },
#endif
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_Advanced.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Use a custom blueprint action menu for creating nodes (very prototype, not supported in 5.0 or earlier)" },
#endif
	};
	static constexpr UECodeGen_Private::FMetaDataPairParam NewProp_bForceRefreshGraphAfterFormatting_MetaData[] = {
		{ "Category", "Misc|Experimental" },
#if !UE_BUILD_SHIPPING
		{ "Comment", "/* Hacky workaround to ensure that default comment nodes will be correctly resized after formatting */" },
#endif
		{ "ModuleRelativePath", "Public/BlueprintAssistSettings_Advanced.h" },
#if !UE_BUILD_SHIPPING
		{ "ToolTip", "Hacky workaround to ensure that default comment nodes will be correctly resized after formatting" },
#endif
	};
#endif // WITH_METADATA
	static void NewProp_bRemoveLoopingCausedBySwapping_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bRemoveLoopingCausedBySwapping;
	static const UECodeGen_Private::FNamePropertyParams NewProp_DisabledCommands_ElementProp;
	static const UECodeGen_Private::FSetPropertyParams NewProp_DisabledCommands;
	static void NewProp_bEnableMaterialGraphPinHoverFix_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bEnableMaterialGraphPinHoverFix;
	static void NewProp_bGenerateUniqueGUIDForMaterialExpressions_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bGenerateUniqueGUIDForMaterialExpressions;
	static void NewProp_bStoreCacheDataInPackageMetaData_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bStoreCacheDataInPackageMetaData;
	static void NewProp_bPrettyPrintCacheJSON_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bPrettyPrintCacheJSON;
	static void NewProp_bUseCustomBlueprintActionMenu_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bUseCustomBlueprintActionMenu;
	static void NewProp_bForceRefreshGraphAfterFormatting_SetBit(void* Obj);
	static const UECodeGen_Private::FBoolPropertyParams NewProp_bForceRefreshGraphAfterFormatting;
	static const UECodeGen_Private::FPropertyParamsBase* const PropPointers[];
	static UObject* (*const DependentSingletons[])();
	static constexpr FCppClassTypeInfoStatic StaticCppClassTypeInfo = {
		TCppClassTypeTraits<UBASettings_Advanced>::IsAbstract,
	};
	static const UECodeGen_Private::FClassParams ClassParams;
};
void Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_bRemoveLoopingCausedBySwapping_SetBit(void* Obj)
{
	((UBASettings_Advanced*)Obj)->bRemoveLoopingCausedBySwapping = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_bRemoveLoopingCausedBySwapping = { "bRemoveLoopingCausedBySwapping", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(UBASettings_Advanced), &Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_bRemoveLoopingCausedBySwapping_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bRemoveLoopingCausedBySwapping_MetaData), NewProp_bRemoveLoopingCausedBySwapping_MetaData) };
const UECodeGen_Private::FNamePropertyParams Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_DisabledCommands_ElementProp = { "DisabledCommands", nullptr, (EPropertyFlags)0x0000000000004001, UECodeGen_Private::EPropertyGenFlags::Name, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, 0, METADATA_PARAMS(0, nullptr) };
const UECodeGen_Private::FSetPropertyParams Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_DisabledCommands = { "DisabledCommands", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Set, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, STRUCT_OFFSET(UBASettings_Advanced, DisabledCommands), METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_DisabledCommands_MetaData), NewProp_DisabledCommands_MetaData) };
void Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_bEnableMaterialGraphPinHoverFix_SetBit(void* Obj)
{
	((UBASettings_Advanced*)Obj)->bEnableMaterialGraphPinHoverFix = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_bEnableMaterialGraphPinHoverFix = { "bEnableMaterialGraphPinHoverFix", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(UBASettings_Advanced), &Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_bEnableMaterialGraphPinHoverFix_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bEnableMaterialGraphPinHoverFix_MetaData), NewProp_bEnableMaterialGraphPinHoverFix_MetaData) };
void Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_bGenerateUniqueGUIDForMaterialExpressions_SetBit(void* Obj)
{
	((UBASettings_Advanced*)Obj)->bGenerateUniqueGUIDForMaterialExpressions = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_bGenerateUniqueGUIDForMaterialExpressions = { "bGenerateUniqueGUIDForMaterialExpressions", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(UBASettings_Advanced), &Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_bGenerateUniqueGUIDForMaterialExpressions_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bGenerateUniqueGUIDForMaterialExpressions_MetaData), NewProp_bGenerateUniqueGUIDForMaterialExpressions_MetaData) };
void Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_bStoreCacheDataInPackageMetaData_SetBit(void* Obj)
{
	((UBASettings_Advanced*)Obj)->bStoreCacheDataInPackageMetaData = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_bStoreCacheDataInPackageMetaData = { "bStoreCacheDataInPackageMetaData", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(UBASettings_Advanced), &Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_bStoreCacheDataInPackageMetaData_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bStoreCacheDataInPackageMetaData_MetaData), NewProp_bStoreCacheDataInPackageMetaData_MetaData) };
void Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_bPrettyPrintCacheJSON_SetBit(void* Obj)
{
	((UBASettings_Advanced*)Obj)->bPrettyPrintCacheJSON = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_bPrettyPrintCacheJSON = { "bPrettyPrintCacheJSON", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(UBASettings_Advanced), &Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_bPrettyPrintCacheJSON_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bPrettyPrintCacheJSON_MetaData), NewProp_bPrettyPrintCacheJSON_MetaData) };
void Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_bUseCustomBlueprintActionMenu_SetBit(void* Obj)
{
	((UBASettings_Advanced*)Obj)->bUseCustomBlueprintActionMenu = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_bUseCustomBlueprintActionMenu = { "bUseCustomBlueprintActionMenu", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(UBASettings_Advanced), &Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_bUseCustomBlueprintActionMenu_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bUseCustomBlueprintActionMenu_MetaData), NewProp_bUseCustomBlueprintActionMenu_MetaData) };
void Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_bForceRefreshGraphAfterFormatting_SetBit(void* Obj)
{
	((UBASettings_Advanced*)Obj)->bForceRefreshGraphAfterFormatting = 1;
}
const UECodeGen_Private::FBoolPropertyParams Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_bForceRefreshGraphAfterFormatting = { "bForceRefreshGraphAfterFormatting", nullptr, (EPropertyFlags)0x0010000000004001, UECodeGen_Private::EPropertyGenFlags::Bool | UECodeGen_Private::EPropertyGenFlags::NativeBool, RF_Public|RF_Transient|RF_MarkAsNative, nullptr, nullptr, 1, sizeof(bool), sizeof(UBASettings_Advanced), &Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_bForceRefreshGraphAfterFormatting_SetBit, METADATA_PARAMS(UE_ARRAY_COUNT(NewProp_bForceRefreshGraphAfterFormatting_MetaData), NewProp_bForceRefreshGraphAfterFormatting_MetaData) };
const UECodeGen_Private::FPropertyParamsBase* const Z_Construct_UClass_UBASettings_Advanced_Statics::PropPointers[] = {
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_bRemoveLoopingCausedBySwapping,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_DisabledCommands_ElementProp,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_DisabledCommands,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_bEnableMaterialGraphPinHoverFix,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_bGenerateUniqueGUIDForMaterialExpressions,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_bStoreCacheDataInPackageMetaData,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_bPrettyPrintCacheJSON,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_bUseCustomBlueprintActionMenu,
	(const UECodeGen_Private::FPropertyParamsBase*)&Z_Construct_UClass_UBASettings_Advanced_Statics::NewProp_bForceRefreshGraphAfterFormatting,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_UBASettings_Advanced_Statics::PropPointers) < 2048);
UObject* (*const Z_Construct_UClass_UBASettings_Advanced_Statics::DependentSingletons[])() = {
	(UObject* (*)())Z_Construct_UClass_UObject,
	(UObject* (*)())Z_Construct_UPackage__Script_BlueprintAssist,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_UBASettings_Advanced_Statics::DependentSingletons) < 16);
const UECodeGen_Private::FClassParams Z_Construct_UClass_UBASettings_Advanced_Statics::ClassParams = {
	&UBASettings_Advanced::StaticClass,
	"EditorPerProjectUserSettings",
	&StaticCppClassTypeInfo,
	DependentSingletons,
	nullptr,
	Z_Construct_UClass_UBASettings_Advanced_Statics::PropPointers,
	nullptr,
	UE_ARRAY_COUNT(DependentSingletons),
	0,
	UE_ARRAY_COUNT(Z_Construct_UClass_UBASettings_Advanced_Statics::PropPointers),
	0,
	0x001000A4u,
	METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UClass_UBASettings_Advanced_Statics::Class_MetaDataParams), Z_Construct_UClass_UBASettings_Advanced_Statics::Class_MetaDataParams)
};
UClass* Z_Construct_UClass_UBASettings_Advanced()
{
	if (!Z_Registration_Info_UClass_UBASettings_Advanced.OuterSingleton)
	{
		UECodeGen_Private::ConstructUClass(Z_Registration_Info_UClass_UBASettings_Advanced.OuterSingleton, Z_Construct_UClass_UBASettings_Advanced_Statics::ClassParams);
	}
	return Z_Registration_Info_UClass_UBASettings_Advanced.OuterSingleton;
}
template<> BLUEPRINTASSIST_API UClass* StaticClass<UBASettings_Advanced>()
{
	return UBASettings_Advanced::StaticClass();
}
DEFINE_VTABLE_PTR_HELPER_CTOR(UBASettings_Advanced);
UBASettings_Advanced::~UBASettings_Advanced() {}
// End Class UBASettings_Advanced

// Begin Registration
struct Z_CompiledInDeferFile_FID_TA_Lesson_Plugins_BlueprintAssist_Source_BlueprintAssist_Public_BlueprintAssistSettings_Advanced_h_Statics
{
	static constexpr FClassRegisterCompiledInInfo ClassInfo[] = {
		{ Z_Construct_UClass_UBASettings_Advanced, UBASettings_Advanced::StaticClass, TEXT("UBASettings_Advanced"), &Z_Registration_Info_UClass_UBASettings_Advanced, CONSTRUCT_RELOAD_VERSION_INFO(FClassReloadVersionInfo, sizeof(UBASettings_Advanced), 3664498485U) },
	};
};
static FRegisterCompiledInInfo Z_CompiledInDeferFile_FID_TA_Lesson_Plugins_BlueprintAssist_Source_BlueprintAssist_Public_BlueprintAssistSettings_Advanced_h_1038123382(TEXT("/Script/BlueprintAssist"),
	Z_CompiledInDeferFile_FID_TA_Lesson_Plugins_BlueprintAssist_Source_BlueprintAssist_Public_BlueprintAssistSettings_Advanced_h_Statics::ClassInfo, UE_ARRAY_COUNT(Z_CompiledInDeferFile_FID_TA_Lesson_Plugins_BlueprintAssist_Source_BlueprintAssist_Public_BlueprintAssistSettings_Advanced_h_Statics::ClassInfo),
	nullptr, 0,
	nullptr, 0);
// End Registration
PRAGMA_ENABLE_DEPRECATION_WARNINGS
