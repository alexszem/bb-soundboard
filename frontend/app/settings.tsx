import { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Alert } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function Settings() {
  const [url, setUrl] = useState('');

  useEffect(() => {
    const loadUrl = async () => {
      const savedUrl = await AsyncStorage.getItem('api_url');
      if (savedUrl) setUrl(savedUrl);
    };
    loadUrl();
  }, []);

  const saveUrl = async () => {
    await AsyncStorage.setItem('api_url', url);
    Alert.alert('Success', 'API URL saved successfully');
  };

  return (
    <View style={styles.container}>
      <Text style={styles.label}>API URL</Text>
      <TextInput
        style={styles.input}
        value={url}
        onChangeText={setUrl}
        placeholder="http://192.168.1.100:8000"
      />
      <Button title="Save URL" onPress={saveUrl} />
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
  label: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 8,
    borderRadius: 4,
  },
});