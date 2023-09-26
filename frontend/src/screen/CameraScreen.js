import { Platform, View, Text, Image, Button, Alert, StyleSheet, ScrollView, Dimensions } from 'react-native'
import React, { Fragment, useState, useEffect } from 'react'
// import MenuButtonItem from '../Components/MenuButtonItem';
import { launchImageLibrary } from 'react-native-image-picker';
import MapView, { PROVIDER_GOOGLE, Marker } from 'react-native-maps';
import axios from 'axios';
import FuegoIcon from '../../assets/FuegoIcon.png'
import HospitalColumbus from '../../assets/HospitalColumbus.jpg'
import Limpiar from "../../assets/Limpiar.png"
import IconDanger from "../../assets/IconDanger.png"
import FrioIcon from "../../assets/FrioIcon.png"
import MenuButtonItem from '../Components/MenuButtonItem';
import * as Location from 'expo-location';
import CuidadosIcon from '../../assets/CuiadosIcon.png';
import hospitalIcon from '../../assets/HospitalIcon.png'

// import AnalisisResultScreen from './AnalisisResultScreen';

const CameraScreen = () => {

  const [image, setImage] = useState('https://fakeimg.pl/350x200/?text=No Image&font=Lato')
  const [hospitalInfo, setHospitalInfo] = useState('Se necsita informacion para mostrar este mensaje')
  const [resultadoInfo, setResultadoInfo] = useState('Se necsita informacion para mostrar este mensaje')
  const [primerCuidados, setPrimerCuidados] = useState('Se necsita informacion para mostrar este mensaje')
  const [segundoCuidados, setSegundoCuidados] = useState('Se necsita informacion para mostrar este mensaje')
  const [tercerCuidados, setTercerCuidados] = useState('Se necsita informacion para mostrar este mensaje')
  const [cuartoCuidados, setCuartoCuidados] = useState('Se necsita informacion para mostrar este mensaje')
  const [quintoCuidados, setQuintoCuidados] = useState('Se necsita informacion para mostrar este mensaje')
  const [visible, setVisible] = useState(false);
  const [ifPrimerGrado, setIfPrimerGrado] = useState(false);
  const [latitud, setLatitud] = useState(null);
  const [longitud, setLongitud] = useState(null);

  const [time, setTime] = React.useState(null)
  const [location, setLocation] = React.useState(null);
  const [errorMsg, setErrorMsg] = React.useState(null);

  React.useEffect(() => {
    (async () => {
      let { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        setErrorMsg('Permission to access location was denied');
        return;
      }
      const before = new Date()
      let location = await Location.getCurrentPositionAsync();
      const after = new Date()
      setLocation(location);

      //const seconds = (after.getTime() - before.getTime()) / 1000

      //setTime(`in ${seconds} seconds`)
    })();
  }, []);

  let text = 'Waiting..';
  if (errorMsg) {
    text = errorMsg;
  } else if (location) {
    text = JSON.stringify(location);
  }

  const [imageBase64, setImageBase64] = useState('');
  const API_SCHEMA = 'http';
  const API_HOST = 'backend-app-124923626.us-east-1.elb.amazonaws.com';
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

    const latitud = JSON.stringify(location?.coords?.latitude)
    const longitud = JSON.stringify(location?.coords?.longitude)
    const response = await uploadImage({
      img: imageBase64,
      coordenadas: `${latitud}%2C${longitud}`,
    })
    console.log(response.data);
    if (response) {
      var responseText = response.data
      const parsedJson = JSON.parse(responseText)
      const cuidados = parsedJson.cuidados
      const resultado = parsedJson.resultado
      const hospital = parsedJson.hospital.nombre
      const latitud = parsedJson.hospital.coordenadas.lat
      const longitud = parsedJson.hospital.coordenadas.lng
      const primerCuidado = cuidados[0];
      const segundoCuidado = cuidados[1];
      const tercerCuidado = cuidados[2];
      const cuartoCuidado = cuidados[3];
      const quintoCuidado = cuidados[4];
      setLatitud(latitud)
      setLongitud(longitud)
      setHospitalInfo(hospital)
      setResultadoInfo(resultado)
      setPrimerCuidados(primerCuidado)
      setSegundoCuidados(segundoCuidado)
      setTercerCuidados(tercerCuidado)
      setCuartoCuidados(cuartoCuidado)
      setQuintoCuidados(quintoCuidado)
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

  const markregion = {
    latitude: latitud,
    longitude: longitud,
    latitudeDelta: 0.0922,
    longitudeDelta: 0.0421,
  }

  return (
    <ScrollView
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

              <View style = { styles.identificacionContainer }>
                <Text style = { styles.subTitleTextIdent }>
                  Gravedad de quemadura
                </Text>
                <View style={styles.row}>
                  <View style={[styles.box7, styles.box6]}>
                    <Image
                      source={IconDanger}
                      style={styles.identImg}
                    />
                  </View> 
                  <View style={[styles.box7]}>
                    <Text style = { styles.identText }>
                      {resultadoInfo}
                    </Text>
                  </View> 
                </View>
                <Text>

                </Text>
              </View>

              <View style = { styles.identificacionContainer }>
                <Text style = { styles.subTitleTextIdent }>
                  Te recomendamos...
                </Text>
                <View style={styles.row}>
                  <View style={[styles.box7, styles.box6]}>
                    <Image
                      source={CuidadosIcon}
                      style={styles.identImg}
                    />
                  </View>
                  <Text>

                  </Text>
                  <View style={[styles.box7]}>
                    <Text style = { styles.cuidadosText }>
                      {primerCuidados}
                    </Text>
                    <Text style = { styles.cuidadosText }>
                      {segundoCuidados}
                    </Text>
                    <Text style = { styles.cuidadosText }>
                      {tercerCuidados}
                    </Text>
                    <Text style = { styles.cuidadosText }>
                      {cuartoCuidados}
                    </Text>
                    <Text style = { styles.cuidadosText }>
                      {quintoCuidados}
                    </Text>
                  </View>
                  <Text>
                    
                  </Text> 
                </View>
                <Text>

                </Text>
              </View>

              <View style = { styles.identificacionContainer }>
                <Text style = { styles.subTitleTextIdent }>
                  Hospital más cercano
                </Text>
                <View style={styles.row}>
                  <View style={[styles.box7, styles.box6]}>
                    <Image
                      source={hospitalIcon}
                      style={styles.identImg}
                    />
                  </View> 
                  <View style={[styles.box7]}>
                    <Text style = { styles.identText }>
                      {hospitalInfo}
                    </Text>
                    <Text style = { styles.cuidadosText }>
                      NOTA: Solo ve al hospital si tu herida empeora
                    </Text>
                  </View> 
                </View>
                <Text>

                </Text>
              </View>
              <Text>{''}</Text>
              <View alignItems='center'>
                <MenuButtonItem text={'Regresar'} onPress={() => setVisible(false)}>

                </MenuButtonItem>
              </View>
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

              <View style = { styles.identificacionContainer }>
                <Text style = { styles.subTitleTextIdent }>
                  Gravedad de quemadura
                </Text>
                <View style={styles.row}>
                  <View style={[styles.box7, styles.box6]}>
                    <Image
                      source={IconDanger}
                      style={styles.identImg}
                    />
                  </View> 
                  <View style={[styles.box7]}>
                    <Text style = { styles.identText }>
                      {resultadoInfo}
                    </Text>
                  </View> 
                </View>
                <Text>

                </Text>
              </View>

              <View style = { styles.identificacionContainer }>
                <Text style = { styles.subTitleTextIdent }>
                  Te recomendamos...
                </Text>
                <View style={styles.row}>
                  <View style={[styles.box7, styles.box6]}>
                    <Image
                      source={CuidadosIcon}
                      style={styles.identImg}
                    />
                  </View>
                  <Text>

                  </Text>
                  <View style={[styles.box7]}>
                    <Text style = { styles.cuidadosText }>
                      {primerCuidados}
                    </Text>
                    <Text style = { styles.cuidadosText }>
                      {segundoCuidados}
                    </Text>
                    <Text style = { styles.cuidadosText }>
                      {tercerCuidados}
                    </Text>
                    <Text style = { styles.cuidadosText }>
                      {cuartoCuidados}
                    </Text>
                    <Text style = { styles.cuidadosText }>
                      {quintoCuidados}
                    </Text>
                  </View>
                  <Text>
                    
                  </Text> 
                </View>
                <Text>

                </Text>
              </View>

              <View style = { styles.identificacionContainer }>
                <Text style = { styles.subTitleTextIdent }>
                  Hospital más cercano
                </Text>
                <View style={styles.row}>
                  <View style={[styles.box7, styles.box6]}>
                    <Image
                      source={hospitalIcon}
                      style={styles.identImg}
                    />
                  </View> 
                  <View style={[styles.box7]}>
                    <Text style = { styles.identText }>
                      {hospitalInfo}
                    </Text>
                    <Text style = { styles.cuidadosText }>
                      NOTA: El marker azul es tu ubicación actual, el rojo el centro medico mas cercano
                    </Text>
                  </View> 
                </View>
                <Text>

                </Text>
              </View>

                <View style={{
                  flex: 1,
                  backgroundColor: '#fff',
                  alignItems: 'center',
                  justifyContent: 'center', 
                }}>
                  <MapView
                    provider={PROVIDER_GOOGLE}
                    style={{ 
                      width: Dimensions.get('window').width,
                      height: Dimensions.get('window').height,
                    }}
                    region={{
                      latitude: latitud,
                      longitude: longitud,
                      latitudeDelta: 0.0922,
                      longitudeDelta: 0.0421,
                    }}
                    zoomEnabled={true}
                    showsUserLocation={true}
                  >
                    <Marker coordinate={markregion} />
                  </MapView>
                </View>
              <Text>{''}</Text>
              <View alignItems='center'>
                <MenuButtonItem text={'Regresar'} onPress={() => setVisible(false)}>

                </MenuButtonItem>
              </View>
            </>
          )}

        </>
      ) : (
        <>
          <View alignItems='center'>
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
            <Text>
                {"              Latitud: "}{text}
            </Text>
            <Text>
                {"              Latitud: "}{time}
            </Text>
            
          </View>

        </>
      )}

    </ScrollView>

  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 24,
    backgroundColor: '#eaeaea',
  },
  container2: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
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
  map: {
    width: Dimensions.get('window').width,
    height: Dimensions.get('window').height,
  },

  identImg: {
    // marginStart: 35,
    marginTop: 30,
    borderRadius: 30,
    height: 70,
    width: 70,
    alignSelf: 'center',
  },

  subTitleTextIdent: {
    marginStart: 15,
    color: '#7F2413',
    fontFamily: 'Raleway-SemiBold',
    textAlign: 'left',
    fontSize: 20,
  },

  cuidadosText: {
    color: '#000000',
    fontFamily: 'Raleway-SemiBold',
    textAlign: 'left',
    fontSize: 15,
    marginTop: 50,
    marginStart: 25
  },

  identText: {
    color: '#000000',
    fontFamily: 'Raleway-SemiBold',
    textAlign: 'left',
    fontSize: 25,
    marginTop: 50,
    marginStart: 25
  },

  box6: {
    flex: 1,
    height: 100,
    backgroundColor: '#F5F5F5',
  },
  box7: {
    flex: 3,
    backgroundColor: '#F5F5F5'
  },
  row: {
    flex: 1,
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 10
  },
  

})



export default CameraScreen