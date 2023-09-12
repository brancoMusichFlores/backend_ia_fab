import { View, Text, TouchableOpacity, StyleSheet, Image } from 'react-native'
import React from 'react'

const MenuButtonItem = ({ text, onPress}) => {
  return (
    <TouchableOpacity
        style = { styles.buttonContainer }
        onPress={ onPress }
    >

      <Text style = { styles.text }>{ text }</Text>
    </TouchableOpacity>
  )
}

const styles = StyleSheet.create({

    buttonContainer: {
        alignItems: 'center',
        backgroundColor: '#7F2413',
        borderRadius: 10,
        flexDirection: 'center',
        marginBottom: 10,
        padding: 10,
        width: "50%",
    },

    text: {
      marginStart: 15,
      color: '#FFFFFF'
    },

})

export default MenuButtonItem
