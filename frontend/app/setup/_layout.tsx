import { Stack, usePathname } from "expo-router";

export default function Layout() {
  // const pathname = usePathname();

  return (
    <Stack
      // screenOptions={{
      //   animation: pathname.startsWith("/songs") ? "default" : "none",
      // }}
    >
      <Stack.Screen name="index" options={{ headerShown: false}} />
      <Stack.Screen name="songs" options={{ title: "Songs" }} />
      <Stack.Screen name="lineup" options={{ title: "Lineup" }} />
      <Stack.Screen name="usage" options={{ title: "Usage" }} />
    </Stack>
  );
}