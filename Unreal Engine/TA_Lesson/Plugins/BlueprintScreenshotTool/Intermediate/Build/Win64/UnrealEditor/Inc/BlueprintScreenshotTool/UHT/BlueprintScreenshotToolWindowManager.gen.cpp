// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "BlueprintScreenshotTool/Public/BlueprintScreenshotToolWindowManager.h"
PRAGMA_DISABLE_DEPRECATION_WARNINGS
void EmptyLinkFunctionForGeneratedCodeBlueprintScreenshotToolWindowManager() {}

// Begin Cross Module References
BLUEPRINTSCREENSHOTTOOL_API UClass* Z_Construct_UClass_UBlueprintScreenshotToolWindowManager();
BLUEPRINTSCREENSHOTTOOL_API UClass* Z_Construct_UClass_UBlueprintScreenshotToolWindowManager_NoRegister();
COREUOBJECT_API UClass* Z_Construct_UClass_UObject();
UPackage* Z_Construct_UPackage__Script_BlueprintScreenshotTool();
// End Cross Module References

// Begin Class UBlueprintScreenshotToolWindowManager
void UBlueprintScreenshotToolWindowManager::StaticRegisterNativesUBlueprintScreenshotToolWindowManager()
{
}
IMPLEMENT_CLASS_NO_AUTO_REGISTRATION(UBlueprintScreenshotToolWindowManager);
UClass* Z_Construct_UClass_UBlueprintScreenshotToolWindowManager_NoRegister()
{
	return UBlueprintScreenshotToolWindowManager::StaticClass();
}
struct Z_Construct_UClass_UBlueprintScreenshotToolWindowManager_Statics
{
#if WITH_METADATA
	static constexpr UECodeGen_Private::FMetaDataPairParam Class_MetaDataParams[] = {
		{ "IncludePath", "BlueprintScreenshotToolWindowManager.h" },
		{ "ModuleRelativePath", "Public/BlueprintScreenshotToolWindowManager.h" },
	};
#endif // WITH_METADATA
	static UObject* (*const DependentSingletons[])();
	static constexpr FCppClassTypeInfoStatic StaticCppClassTypeInfo = {
		TCppClassTypeTraits<UBlueprintScreenshotToolWindowManager>::IsAbstract,
	};
	static const UECodeGen_Private::FClassParams ClassParams;
};
UObject* (*const Z_Construct_UClass_UBlueprintScreenshotToolWindowManager_Statics::DependentSingletons[])() = {
	(UObject* (*)())Z_Construct_UClass_UObject,
	(UObject* (*)())Z_Construct_UPackage__Script_BlueprintScreenshotTool,
};
static_assert(UE_ARRAY_COUNT(Z_Construct_UClass_UBlueprintScreenshotToolWindowManager_Statics::DependentSingletons) < 16);
const UECodeGen_Private::FClassParams Z_Construct_UClass_UBlueprintScreenshotToolWindowManager_Statics::ClassParams = {
	&UBlueprintScreenshotToolWindowManager::StaticClass,
	nullptr,
	&StaticCppClassTypeInfo,
	DependentSingletons,
	nullptr,
	nullptr,
	nullptr,
	UE_ARRAY_COUNT(DependentSingletons),
	0,
	0,
	0,
	0x001000A0u,
	METADATA_PARAMS(UE_ARRAY_COUNT(Z_Construct_UClass_UBlueprintScreenshotToolWindowManager_Statics::Class_MetaDataParams), Z_Construct_UClass_UBlueprintScreenshotToolWindowManager_Statics::Class_MetaDataParams)
};
UClass* Z_Construct_UClass_UBlueprintScreenshotToolWindowManager()
{
	if (!Z_Registration_Info_UClass_UBlueprintScreenshotToolWindowManager.OuterSingleton)
	{
		UECodeGen_Private::ConstructUClass(Z_Registration_Info_UClass_UBlueprintScreenshotToolWindowManager.OuterSingleton, Z_Construct_UClass_UBlueprintScreenshotToolWindowManager_Statics::ClassParams);
	}
	return Z_Registration_Info_UClass_UBlueprintScreenshotToolWindowManager.OuterSingleton;
}
template<> BLUEPRINTSCREENSHOTTOOL_API UClass* StaticClass<UBlueprintScreenshotToolWindowManager>()
{
	return UBlueprintScreenshotToolWindowManager::StaticClass();
}
UBlueprintScreenshotToolWindowManager::UBlueprintScreenshotToolWindowManager(const FObjectInitializer& ObjectInitializer) : Super(ObjectInitializer) {}
DEFINE_VTABLE_PTR_HELPER_CTOR(UBlueprintScreenshotToolWindowManager);
UBlueprintScreenshotToolWindowManager::~UBlueprintScreenshotToolWindowManager() {}
// End Class UBlueprintScreenshotToolWindowManager

// Begin Registration
struct Z_CompiledInDeferFile_FID_HostProject_Plugins_BlueprintScreenshotTool_Source_BlueprintScreenshotTool_Public_BlueprintScreenshotToolWindowManager_h_Statics
{
	static constexpr FClassRegisterCompiledInInfo ClassInfo[] = {
		{ Z_Construct_UClass_UBlueprintScreenshotToolWindowManager, UBlueprintScreenshotToolWindowManager::StaticClass, TEXT("UBlueprintScreenshotToolWindowManager"), &Z_Registration_Info_UClass_UBlueprintScreenshotToolWindowManager, CONSTRUCT_RELOAD_VERSION_INFO(FClassReloadVersionInfo, sizeof(UBlueprintScreenshotToolWindowManager), 3378852875U) },
	};
};
static FRegisterCompiledInInfo Z_CompiledInDeferFile_FID_HostProject_Plugins_BlueprintScreenshotTool_Source_BlueprintScreenshotTool_Public_BlueprintScreenshotToolWindowManager_h_2258427280(TEXT("/Script/BlueprintScreenshotTool"),
	Z_CompiledInDeferFile_FID_HostProject_Plugins_BlueprintScreenshotTool_Source_BlueprintScreenshotTool_Public_BlueprintScreenshotToolWindowManager_h_Statics::ClassInfo, UE_ARRAY_COUNT(Z_CompiledInDeferFile_FID_HostProject_Plugins_BlueprintScreenshotTool_Source_BlueprintScreenshotTool_Public_BlueprintScreenshotToolWindowManager_h_Statics::ClassInfo),
	nullptr, 0,
	nullptr, 0);
// End Registration
PRAGMA_ENABLE_DEPRECATION_WARNINGS
