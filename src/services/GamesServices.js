import axios from 'axios'
export default {
  fetchPosts (userId) {
    return axios.get('assign?userid=' + userId);
  }
}
