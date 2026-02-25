import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

export default function NuevaTransaccionScreen({ navigation }) {
  const [tipo, setTipo] = useState('ingreso');

  return (
    <View style={styles.container}>
      
      <View style={styles.header}>
        <Ionicons name="wallet-outline" size={28} color="white" />
        <Text style={styles.headerTitle}>Nueva Transacción</Text>
        <Ionicons name="notifications-outline" size={28} color="white" />
      </View>

      <View style={styles.form}>

        <Text style={styles.label}>Cuenta</Text>
        <TextInput 
          style={styles.input} 
          placeholder="Cuenta Principal" 
          placeholderTextColor="#666"
        />

        <Text style={styles.label}>Monto</Text>
        <TextInput 
          style={styles.input} 
          placeholder="0.00" 
          keyboardType="numeric" 
          placeholderTextColor="#666"
        />

        <Text style={styles.label}>Categoría</Text>
        <TextInput 
          style={styles.input} 
          placeholder="Seleccionar categoría" 
          placeholderTextColor="#666"
        />

        <Text style={styles.label}>Fecha</Text>
        <TextInput 
          style={styles.input} 
          placeholder="05/11/2025"
          placeholderTextColor="#666"
        />

        <Text style={styles.label}>Descripción</Text>
        <TextInput
          style={[styles.input, { height: 80 }]}
          placeholder="Descripción de la transacción"
          placeholderTextColor="#666"
          multiline
        />

        <Text style={styles.label}>Tipo</Text>
        <View style={styles.tipoContainer}>
          <TouchableOpacity
            style={[styles.tipoButton, tipo === 'ingreso' && styles.tipoActivo]}
            onPress={() => setTipo('ingreso')}
          >
            <Text style={[styles.tipoText, tipo === 'ingreso' && styles.tipoTextActivo]}>
              Ingreso
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.tipoButton, tipo === 'gasto' && styles.tipoActivo]}
            onPress={() => setTipo('gasto')}
          >
            <Text style={[styles.tipoText, tipo === 'gasto' && styles.tipoTextActivo]}>
              Gasto
            </Text>
          </TouchableOpacity>
        </View>

        <TouchableOpacity
          style={styles.saveButton}
          onPress={() => navigation.goBack()}
        >
          <Text style={styles.saveText}>Guardar Transacción</Text>
        </TouchableOpacity>

      </View>

    </View>
  );
}

const styles = StyleSheet.create({
  container: { 
    flex: 1, 
    backgroundColor: '#fff',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#006400',
    padding: 20,
    borderBottomLeftRadius: 25,
    borderBottomRightRadius: 25,
  },
  headerTitle: { 
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 18 
  },
  form: { 
    padding: 20 
  },
  label: { 
    fontWeight: 'bold', 
    fontSize: 15,
    color: '#222',
    marginTop: 10,
  },
  input: {
    borderWidth: 1,
    borderColor: '#aaa',
    borderRadius: 10,
    padding: 12,
    marginTop: 5,
    color: '#222',
    fontSize: 15,
  },
  tipoContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginVertical: 15,
  },
  tipoButton: {
    flex: 1,
    borderWidth: 1,
    borderColor: '#00b140',
    borderRadius: 10,
    padding: 12,
    alignItems: 'center',
    marginHorizontal: 5,
  },
  tipoActivo: {
    backgroundColor: '#00b140',
  },
  tipoText: { 
    color: '#00b140', 
    fontWeight: 'bold',
    fontSize: 15,
  },
  tipoTextActivo: { 
    color: 'white' 
  },
  saveButton: {
    backgroundColor: '#00b140',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
    marginTop: 20,
  },
  saveText: { 
    color: 'white', 
    fontWeight: 'bold',
    fontSize: 16
  },
});