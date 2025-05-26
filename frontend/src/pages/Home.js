import NavItem from 'react-bootstrap/esm/NavItem';
import '../App.css';
import tileImg from '../img/image.png';
import Button from 'react-bootstrap/Button';
import Nav from 'react-bootstrap/Nav';

function Home() {
  return (
    <div className='app-container'>
        <header className='Home-header'>
            <h6 style={{marginLeft: 100, fontSize: 24}}>Транспонатор нот</h6>
            <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
                <a style={{fontSize: 24, display: 'flex', justifyContent: 'center', alignItems: 'center', height: 35, background:'white', outlineColor:'white'}}>Вход</a>
                <Button style={{marginLeft: 20, marginRight: 100, fontSize: 24, height: 35, display: 'flex', justifyContent: 'center', alignItems: 'center', color:'#1B9A46', outlineColor: '#1B9A46', background: 'white', borderColor: '#1B9A46'}}>Регистрация</Button>
            </div>
        </header>
        <main className='Home-body'>
            <h4 style={{fontSize: 32}}>Онлайн транспонирование нот</h4>
            <p style={{fontSize: 20}}>Ноты из любого произведения для любого инструмента</p>
            
            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 50}}>
                <div className='Home-tile'>
                    <Button className='Home-tile-button' style={{color:'white', background: '#1B9A46', borderColor: '#1B9A46'}}>Загрузить файл</Button>
                    <p style={{color: '#C8C8C8'}}>Перетащите сюда MP3 файл. Максимальный размер файла - 78 мб</p>
                </div>
            </div>
        </main>
        <footer className='Home-footer'>
            <div style={{color: 'white', padding: '10px'}}>
                huesos.net
            </div>
            <div style={{display: 'flex', justifyContent: 'center'}}>
                <a style={{color:'white', padding: '10px'}}>О нас</a>
                <a style={{color:'white', padding: '10px'}}>Безопасность</a>
                <a style={{color:'white', padding: '10px'}}>Стоимость</a>
                <a style={{color:'white', padding: '10px'}}>Помощь</a>
            </div>
            <div style={{color: 'white', padding: '10px'}}>
                Язык в попе
            </div>
        </footer>
    </div>
  );
}

export default Home;
