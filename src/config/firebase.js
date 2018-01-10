import * as firebase from 'firebase'
require('firebase/firestore')

import config from './firebase.config'
firebase.initializeApp(config)

export default firebase
