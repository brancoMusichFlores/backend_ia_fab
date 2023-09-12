import { View, Text, Image, StyleSheet, Dimensions } from 'react-native'
import React from 'react'
import TrataQuemaduras from '../../assets/TrataQuemaduras.jpg'

const windowWidth = Dimensions.get('screen').width;
const windowHeight = Dimensions.get('screen').height;

const MedicalScreen = () => {
  return (
    <View>
      <Image
        source = { TrataQuemaduras }
        style = { styles.thumbnail }
      />
    </View>
  )
}

const styles = StyleSheet.create({

  thumbnail: {
      width: windowWidth,
      height: windowHeight,
      resizeMode: 'stretch'
  },

})

export default MedicalScreen