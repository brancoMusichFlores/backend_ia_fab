import { View, Text, Image, Button, Alert, StyleSheet } from 'react-native'
import React, { Fragment, useState } from 'react'
// import MenuButtonItem from '../Components/MenuButtonItem';
import { launchCamera, launchImageLibrary } from 'react-native-image-picker';
import axios from 'axios';
import FuegoIcon from '../../assets/FuegoIcon.png'
import HospitalColumbus from '../../assets/HospitalColumbus.jpg'
import Limpiar from "../../assets/Limpiar.png"
import IconDanger from "../../assets/IconDanger.png"
import FrioIcon from "../../assets/FrioIcon.png"
import MenuButtonItem from '../Components/MenuButtonItem';
// import AnalisisResultScreen from './AnalisisResultScreen';

const CameraScreen = () => {

  const [image, setImage] = useState('https://fakeimg.pl/350x200/?text=No Image&font=Lato')
  const [hospitalInfo, setHospitalInfo] = useState('Se necsita informacion para mostrar este mensaje')
  const [resultadoInfo, setResultadoInfo] = useState('Se necsita informacion para mostrar este mensaje')
  const [cuidadoInfo, setCuidadoInfo] = useState('Se necsita informacion para mostrar este mensaje')
  const [visible, setVisible] = useState(false);
  const [ifPrimerGrado, setIfPrimerGrado] = useState(false);

  const [imageBase64, setImageBase64] = useState('');

  const API_SCHEMA = 'http';
  const API_HOST = 'backend-app-879124513.us-east-1.elb.amazonaws.com';
  const API_PATH = '/';

  const headers = {
    'Content-Type': 'application/json',
    'Accept-Language': 'es',
  }

  const httpConfig = {
    baseURL: `${API_SCHEMA}://${API_HOST}${API_PATH}`,
    headers,
  }

  const HTTP = axios.create(httpConfig);

  const uploadImage = async (payload) => {
    try {
      const response = await HTTP.post('analisis/', payload);
      if (response) {
        console.log('Peticion hecha correctamente');
        return response;
      }
    } catch (error) {
      console.log(error);
    }


  };

  const uploadImageMethod = async () => {
    const response = await uploadImage({
      img: imageBase64,
      coordenadas: `20.7635827%2C-103.4396285`,
    })
    console.log(response.data);
    if (response) {
      var responseText = response.data
      const parsedJson = JSON.parse(responseText)
      const cuidados = parsedJson.cuidados
      const resultado = parsedJson.resultado
      const hospital = parsedJson.hospital
      setHospitalInfo(hospital)
      setResultadoInfo(resultado)
      setCuidadoInfo(cuidados)
      if (resultado === "Primer grado"){
        setIfPrimerGrado(true)
      }
      setVisible(true)
    } else {
      setHospitalInfo('Hubo un error en el analisis intenta de nuevo')
    }
  };

  const createTwoButtonAlert = () =>
    Alert.alert('Analizando imagen', 'Espere mientras conseguimos su resultado', [
      {
        text: 'Cancelar',
        onPress: () => console.log('Cancel Pressed'),
        style: 'cancel',
      },
      { text: 'Resultado', onPress: () => Alert.alert('Resultado Obtenido', 'El analisis dio que tienes una quemadura de 3er grado') },
    ]);

  const selectImage = () => {

    const options = {
      title: 'Selecciona una imagen',
      mediaType: 'photo',
      includeBase64: true,
    }

    launchImageLibrary(options, response => {
      if (response.errorCode) {
        console.log(response.errorMessage)
      } else if (response.didCancel) {
        console.log('El usuario cancelo la opcion')
      } else {

        const uri = response.assets[0].uri
        setImage(uri)
        setImageBase64(response.assets[0].base64)
      }
    })

  }


  return (
    <View
    alignItems='center'
    >
      {visible ? (
        <>
          {ifPrimerGrado ? (
            <>
              <Image
                style={{
                  alignSelf: 'center',
                  height: 120,
                  width: 120,
                }}
                source={FuegoIcon}
              />
              <Text style={styles.title}>
                {' '}El resultado ha dado lo siguiente{' '}
              </Text>
              <Text>{''}</Text>
              <Text style={styles.subTitle}>
                Gravedad de quemadura
              </Text>
              <Image
                source={IconDanger}
                style={styles.hospitalImage}
              />
              <Text>{''}</Text>
              <Text>
                {"                    "}{resultadoInfo}
              </Text>
              <Text>{''}</Text>
              <Text style={styles.subTitle}>
                Te recomendamos...
              </Text>
              <Text>{''}</Text>
              <Image
                source={Limpiar}
                style={styles.hospitalImage}
              />
              <Text></Text>
              <Text>
                {"                    "}Limpiar Suavemente
              </Text>
              <Image
                source={FrioIcon}
                style={styles.hospitalImage}
              />
              <Text>
                {"                    "}Enfriar la quemadura
              </Text>
              <Text>{''}</Text>
              <Text style={styles.subTitle}>
                Hospital más cercano
              </Text>
              <Text>{''}</Text>
              <Image
                source={HospitalColumbus}
                style={styles.hospitalImage}
              />
              <Text style={{ fontSize: 20 }}>
                {"              "}{hospitalInfo}
              </Text>
              <Text>{''}</Text>
              <Text>
                {"                    Solo te recomendamos ir a tu hospital más"}
              </Text>
              <Text>
                {"                    cercano si tu herida empeora"}
              </Text>
              <Text>{''}</Text>
              <Button title={'Regresar'} onPress={() => setVisible(false)} />
            </>
          ) : (
            <>
              <Image
                style={{
                  alignSelf: 'center',
                  height: 120,
                  width: 120,
                }}
                source={FuegoIcon}
              />
              <Text style={styles.title}>
                {' '}El resultado ha dado lo siguiente{' '}
              </Text>
              <Text>{''}</Text>
              <Text style={styles.subTitle}>
                Gravedad de quemadura
              </Text>
              <Image
                source={IconDanger}
                style={styles.hospitalImage}
              />
              <Text>{''}</Text>
              <Text>
                {"              "}{resultadoInfo}
              </Text>
              <Text>{''}</Text>
              <Text style={styles.subTitle}>
                Te recomendamos...
              </Text>
              <Text>{''}</Text>
              <Image
                source={Limpiar}
                style={styles.hospitalImage}
              />
              <Text></Text>
              <Text>
                {"              "}Limpiar Suavemente
              </Text>
              <Image
                source={FrioIcon}
                style={styles.hospitalImage}
              />
              <Text>
                {"              "}Enfriar la quemadura
              </Text>
              <Text>{''}</Text>
              <Text style={styles.subTitle}>
                Hospital más cercano
              </Text>
              <Text>{''}</Text>
              <Image
                source={HospitalColumbus}
                style={styles.hospitalImage}
              />
              <Text>
                {"              "}{hospitalInfo}
              </Text>
              <Text>{''}</Text>
              <Button title={'Regresar'} onPress={() => setVisible(false)} />
            </>
          )}

        </>
      ) : (
        <>
          <Image
            style={{
              marginTop: 100,
              alignSelf: 'center',
              height: 200,
              width: 200,
            }}
            source={{ uri: image }}
          />
          <Text>{''}</Text>
          <MenuButtonItem
            text="Seleccionar Imagen"
            onPress={selectImage}
          />
          <Text>{''}</Text>
          <MenuButtonItem text={'Analizar Imagen'} onPress={uploadImageMethod}>

          </MenuButtonItem>
          <Text>{''}</Text>

        </>
      )}

    </View>

  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 24,
    backgroundColor: '#eaeaea',
  },
  title: {
    marginTop: 16,
    paddingVertical: 8,
    borderRadius: 6,
    backgroundColor: '#C1B913',
    color: '#20232a',
    textAlign: 'center',
    fontSize: 25,
    fontWeight: 'bold',
  },
  subTitle: {
    fontWeight: 'bold',
    fontSize: 20,
  },
  hospitalImage: {
    borderRadius: 30,
    height: 30,
    width: 30,
  },
  buttonContainer: {
    alignItems: 'center',
    backgroundColor: '#d9d9d9',
    borderRadius: 10,
    flexDirection: 'row',
    marginBottom: 10,
    padding: 10,
  },
})



export default CameraScreen