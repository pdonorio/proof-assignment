import { Component } from 'react';
import './App.css';

export default class App extends Component {
  state = {
    name: 'some',
  };

  constructor() {
    super();
    this.postArticle = this.postArticle.bind(this);
    this.queryArticle = this.queryArticle.bind(this);
  }

  postArticle(event) {
    event.preventDefault();
    const data = new FormData(event.target);

    fetch('/api/post-article-url', {
      method: 'POST',
      body: data,
    });
  }

  queryArticle(event) {
    event.preventDefault();
    const data = new FormData(event.target);

    fetch('/api/query-article-url', {
      method: 'GET',
      body: data,
    });
  }

  render() {
    return (
      <div className="App">
        <h1>Welcome to {this.state.name}</h1>
        <form onSubmit={this.postArticle}>
          <label htmlFor="url">Add Article URL</label>
          <input id="url" name="url" type="url" />
          <button>Submit Article</button>
        </form>
        <form onSubmit={this.queryArticle}>
          <label htmlFor="url">Add Article URL</label>
          <input id="url" name="url" type="url" />
          <button>Search Articles</button>
        </form>
      </div>
    );
  }
}
