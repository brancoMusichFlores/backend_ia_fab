import React from 'react';
import { DrawerContentScrollView, createDrawerNavigator } from '@react-navigation/drawer';
import CameraScreen from '../screen/CameraScreen';
import MedicalScreen from '../screen/MedicalScreen';
import AboutUsScreen from '../screen/AboutUsScreeen';
import 'react-native-gesture-handler';
import { View } from 'react-native-web';
import { Text, StyleSheet } from 'react-native';
import MenuButtonItem from '../Components/MenuButtonItem';
import MedicalIcon from '../../assets/MedicalIcon.png'
import CameraIcon from '../../assets/CameraIcon.png'

const Drawer = createDrawerNavigator();

export function DrawerNavigation() {
  return (
    <Drawer.Navigator
      drawerContent = { (props) => <MenuItems { ...props} /> }
    >
      <Drawer.Screen name="Camera" component={CameraScreen} />
      <Drawer.Screen name="Medical Info" component={MedicalScreen} />
      <Drawer.Screen name="About Us" component={AboutUsScreen} />
    </Drawer.Navigator>
  );
}

const MenuItems = ({ navigation }) => {

  return (
    <DrawerContentScrollView
      style = { styles.container }
    >
      <Text style = { styles.title }>Menu Principal</Text>
      
      <MenuButtonItem 
        image = { CameraIcon }
        text = "Camera Screen"
        onPress = { () => navigation.navigate('Camera') }
      />

      <MenuButtonItem 
        image = { MedicalIcon }
        text = "Medical Screen"
        onPress = { () => navigation.navigate('Medical Info') }
      />

      <MenuButtonItem 
        text = "About Us"
        onPress = { () => navigation.navigate('About Us') }
      />

    </DrawerContentScrollView>
  )
}

const styles = StyleSheet.create({

  container: {
    padding: 15,
  },

  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 20,
  },

})