var CA = [
    { number: 1, name: 'Camilo'}
    ];
/* global React */    
class AvatarCA extends React.Component{
    render(){
        var url = 'https://avatars2.githubusercontent.com/u/13356409?v=3&s=466';
        return <img src={url} className="mi_imagen"/>
    }
}

class Camilo extends React.Component {
    render(){
        return <li className="letras">
                    <AvatarCA number={ this.props.number } />
                    { this.props.name }
                </li> 
    }
}

class Ctable extends React.Component{
    render(){
        return <ul className="lista">
                {
                    this.props.CA.map((C) => {
                        return <Camilo key={C.number}  name={ C.name } number={ C.number} />
                    })
                }
                </ul>
    }
}

var C = CA[0];

/* global ReactDOM */
ReactDOM.render(
    <Ctable CA={CA} />, 
    document.getElementById('example')
    );