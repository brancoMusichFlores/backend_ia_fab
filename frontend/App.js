import * as React from 'react';
import { Text, View } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import CameraScreen from './src/screen/CameraScreen';
import MedicalScreen from './src/screen/MedicalScreen';
import Ionicons from 'react-native-vector-icons/Ionicons';

function HomeScreen() {
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text>Home!</Text>
    </View>
  );
}

function SettingsScreen() {
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text>Settings!</Text>
    </View>
  );
}

const Tab = createBottomTabNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator
        initialRouteName="Home"
        screenOptions={({ route }) => ({
          tabBarIcon: ({ focused, color, size }) => {
            let iconName;
            let rn = route.name;

            if (rn === "Inicio") {
              iconName = focused ? 'home' : 'home-outline';

            } else if (rn === "Camera") {
              iconName = focused ? 'camera' : 'list-outline';

            } else if (rn === "Settings") {
              iconName = focused ? 'settings' : 'settings-outline';
            }

            // You can return any component that you like here!
            return <Ionicons name={iconName} size={size} color={color} />;
          },
          tabBarActiveTintColor: "#7F2413",
          tabBarInactiveTintColor: "black",
          tabBarLabelStyle: {
            paddingBottom: 10,
            fontSize: 10
          },
          tabBarStyle: [
            {
              "display": "flex"
            },
            null
          ]
        })}
        >

        <Tab.Screen name="Inicio" component={MedicalScreen} />
        <Tab.Screen name="Camera" component={CameraScreen} />
        <Tab.Screen name="Settings" component={SettingsScreen} />

      </Tab.Navigator>
    </NavigationContainer>
  );
}