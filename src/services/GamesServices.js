import axios from 'axios'
export default {
  fetchPosts () {
    return axios.get('assign?userid=12345')
  }
}
