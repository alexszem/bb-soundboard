import { View, Button, StyleSheet } from 'react-native';
import { Link } from 'expo-router';

export default function SetupIndex() {
  return (
    <View style={styles.container}>
      <Link href="/setup/songs" asChild>
        <Button title="Songs" />
      </Link>
      <Link href="/setup/lineup" asChild>
        <Button title="Lineup" />
      </Link>
      <Link href="/setup/usage" asChild>
        <Button title="Usage" />
      </Link>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    gap: 20,
    padding: 16,
  },
});