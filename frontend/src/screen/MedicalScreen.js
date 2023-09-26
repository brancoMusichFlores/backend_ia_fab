import { View, Text, Image, StyleSheet, Dimensions, ScrollView, TouchableOpacity } from 'react-native'
import React from 'react'
import fuego from '../../assets/Fuego.png'
import liquidoCaliente from '../../assets/LiquidoCalienteIcon.png'
import quimicaIcon from '../../assets/QuimicaIcon.png'
import electricidadIcon from '../../assets/ElectricidadIcon.png'
import radiacion from '../../assets/RadiacionIcon.png'
import pielIntacta from '../../assets/PielIntacta.png'
import pielQuemada from '../../assets/PielQuemada.png'

const windowWidth = Dimensions.get('screen').width;
const windowHeight = Dimensions.get('screen').height;

const MedicalScreen = () => {
  return (
    <ScrollView>
      <Text style = { styles.tituloText }>
          Tratamiento De Quemaduras
      </Text>
      <View
        style = { styles.tiposContainer }
      >
        <Text style = { styles.subTitleTextTipos }>
          Tipos
        </Text>
          <View style={styles.row}>
            <View style={[styles.box, styles.box2]}>
              <Image
                source={fuego}
                style={styles.tipoFuego}
              />
              <Text style = { styles.textoFuego }>
                Fuego
              </Text>
            </View>
            <View style={[styles.box, styles.box4]}>
            <Image
                source={quimicaIcon}
                style={styles.tipoFuego}
              />
              <Text style = { styles.textoFuego }>
                Quimicos
              </Text>
            </View> 
            <View style={[styles.box]}>
              <Image
                source={liquidoCaliente}
                style={styles.tipoFuego}
              />
              <Text style = { styles.textoFuego }>
                Liquidos Calientes
              </Text>
            </View> 
            <View style={[styles.box, styles.box3]}>
              <Image
                source={electricidadIcon}
                style={styles.tipoFuego}
              />
              <Text style = { styles.textoFuego }>
                Corriente
              </Text>
            </View>
            <View style={[styles.box, styles.box5]}>
              <Image
                source={radiacion}
                style={styles.tipoFuego}
              />
              <Text style = { styles.textoFuego }>
                Radiacion
              </Text>
            </View> 
          </View>
        <Text>
          
        </Text>
      </View>

      <View style = { styles.identificacionContainer }>
        <Text style = { styles.subTitleTextIdent }>
            Identificación
        </Text>
        <View style={styles.row}>
          <View style={[styles.box7, styles.box6]}>
            <Image
              source={pielIntacta}
              style={styles.identImg}
            />
            <Text style = { styles.identSub }>
              Piel Intacta
            </Text>
          </View> 
          <View style={[styles.box7]}>
            <Text style = { styles.identText }>
              Son superficiales se pueden tratar en casa (Rosaduras, 1er grado).
            </Text>
          </View> 
        </View>
        <Text>

        </Text>

        <View style={styles.row}>
          <View style={[styles.box7, styles.box6]}>
            <Image
              source={pielQuemada}
              style={styles.identImg}
            />
            <Text style = { styles.identSub }>
              Piel Afectada
            </Text>
          </View> 
          <View style={[styles.box7]}>
            <Text style = { styles.identText }>
              Es importante tanto la profunidad y extension, solo las puede atender un profesional. (Ampollas, Heridas Abiertas, 2do y 3er Grado)
            </Text>
            <Text>

            </Text>
          </View> 
        </View>
        <Text>

        </Text>
      </View>
    </ScrollView>
  )
}

const styles = StyleSheet.create({

  tiposContainer: {
    backgroundColor: '#7F2413',
    flexDirection: 'center',
    marginBottom: 10,
    padding: 10,
    width: "100%",
  },

  identificacionContainer: {
    backgroundColor: '#F5F5F5',
    flexDirection: 'center',
    marginBottom: 10,
    padding: 10,
    width: "100%",
  },

  subTitleTextTipos: {
    marginStart: 15,
    color: '#FFFFFF',
    fontFamily: 'Raleway-SemiBold',
    textAlign: 'left',
    fontSize: 30,
  },

  subTitleTextIdent: {
    marginStart: 15,
    color: '#7F2413',
    fontFamily: 'Raleway-SemiBold',
    textAlign: 'left',
    fontSize: 30,
  },

  tituloText: {
    fontFamily: 'JosefinSans-Regular',
    color: '#901414',
    fontSize: 50,
    alignItems: 'flex-start',
  },

  tipoFuego: {
    // marginStart: 35,
    marginTop: 30,
    borderRadius: 30,
    height: 50,
    width: 50,
    alignSelf: 'center',
  },

  identImg: {
    // marginStart: 35,
    marginTop: 30,
    borderRadius: 30,
    height: 70,
    width: 70,
    alignSelf: 'center',
  },

  textoFuego: {
    color: '#F39494',
    fontFamily: 'Raleway-SemiBold',
    textAlign: 'center',
    fontSize: 15,
    marginTop: 15,
  },

  identSub: {
    color: '#F39494',
    fontFamily: 'Raleway-SemiBold',
    textAlign: 'center',
    fontSize: 15,
    marginTop: 15,
  },

  identText: {
    color: '#000000',
    fontFamily: 'Raleway-SemiBold',
    textAlign: 'left',
    fontSize: 15,
    marginTop: 50,
  },

  row: {
    flex: 1,
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 10
  },
  box: {
    flex: 1,
    height: 100,
    backgroundColor: '#7F2413',
  },
  box2: {
    backgroundColor: '#7F2413'
  },
  box3: {
    backgroundColor: '#7F2413'
  },
  box4: {
    backgroundColor: '#7F2413'
  },
  box5: {
    backgroundColor: '#7F2413'
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

})

export default MedicalScreen