import NavItem from 'react-bootstrap/esm/NavItem';
import '../App.css';
import tileImg from '../img/image.png';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import Nav from 'react-bootstrap/Nav';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import { useEffect, useState, useRef } from 'react';
import logImg from '../img/logo.png';
import axios from 'axios';
import gif from '../img/loading.gif'

function Home() {
  const [data, setData] = useState({
    png: '',
    pdf: ''
  });
  const [loading, setLoading] = useState(false);
  const [modalState, setModalState] = useState(false);
  const [modalRegisterState, setModalRegisterState] = useState(false);
  const [alertState1, setAlertState1] = useState(false);
  const [alertState2, setAlertState2] = useState(false);
  const [alertState3, setAlertState3] = useState(false);
  const [alertState4, setAlertState4] = useState(false);
  const [checkToken, setCheckToken] = useState(false);
  const [fileUploadStatus, setFileUploadStatus] = useState(false);
  const fileInputRef = useRef(null); 
  const [loginData, setLoginData] = useState({
    login: '',
    password: ''
  });
  const [registerData, setRegisterData] = useState({
    login: '',
    password: ''
  });

  const handleLoadOpen = () => {fileInputRef.current.click();};
  const handleClose = () => {
    setModalState(false); 
    setAlertState1(false); 
    setAlertState2(false); 
    loginData.login=''; 
    loginData.password='';
  };
  const handleRegisterClose = () => {
    setModalRegisterState(false);
    setAlertState1(false);
    setAlertState2(false);
    registerData.login = '';
    registerData.password = '';
  }
  const handleOpen = (e) => {
    setAlertState1(false);
    setAlertState2(false);
    setAlertState3(false);
    setAlertState4(false);
    if (e.target.tagName == 'A') {
        setModalState(true);
    } else {
        setModalRegisterState(true);
    }
  };
  const handleCheckToken = () => {if (localStorage.getItem('token') != null || localStorage.getItem('token') != '') {setCheckToken(true);} else {setCheckToken(false);}};

  const handleExit = () => {
    localStorage.removeItem('token_expiration');
    localStorage.removeItem('token');
    setCheckToken(false);
    setData(null);
    setLoading(false);
    setFileUploadStatus(false);
    window.location.reload();
  }

  const handleFileChange = async (e) => {
    setLoading(true);
    setFileUploadStatus(false);
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    const token = localStorage.getItem('token');
    try {
        const response = await axios.post('http://localhost:5000/api/transpose/file', formData, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        setLoading(false);
        setFileUploadStatus(true);
        const resp = await axios.get('http://localhost:5000'+response.data.png_url, {
            headers: {
                Authorization: `Bearer ${token}`, 
            },
            responseType: 'blob'
        });
        const pngBlob = new Blob([resp.data], { type: 'image/png' });
        const png_url = URL.createObjectURL(pngBlob); 
        const response_pdf = await axios.get('http://localhost:5000'+response.data.pdf_url, {
            headers: {
                Authorization: `Bearer ${token}`, 
            },
            responseType: 'blob'
        });
        const pdfBlob = new Blob([response_pdf.data], { type: 'application/pdf' });
        const pdf_url = URL.createObjectURL(pdfBlob);
        setData({
            png: png_url,
            pdf: pdf_url,
        });
        console.log(data);
    } catch (error) {
        console.error('Upload failed: ', error);
        if (error.status == 429) {
            setAlertState4(true);
        }
        setLoading(false);
        setFileUploadStatus(false);
    }
  };

  const handleLogin = async () => {
    setModalRegisterState(false);
    setAlertState1(false);
    setAlertState2(false);
    setAlertState3(false);
    const regex = /^.{4,10}$/;
    const regex_login = /^[^ @]{4,20}$/;
    if (regex.test(loginData.password) && regex_login.test(loginData.login)) {
        axios.post('http://localhost:5000/api/login', {username: loginData.login, password: loginData.password})
        .then(response => {
            if (response.data.access_token != null || response.data.access_token != '') {
                const token = response.data.access_token;
                console.log(token);
                const expiresAt = Date.now() + 24 * 60 * 60 * 1000;
                localStorage.setItem('token', token);
                localStorage.setItem('token_expiration', expiresAt);
                window.location.reload();
            }
        })
        .catch(error => {
            if (error.status == 401) {
                setAlertState3(true);
            }
            console.error('Ошибка запроса: ', error);
        })
    } else if (!regex.test(loginData.password)) {
        setAlertState1(true);
    } else if (!regex_login.test(loginData.login)) {
        setAlertState2(true);
    } else {
        handleClose();
    }
  };

  const handleRegister = async () => {
    setModalState(false);
    setAlertState1(false);
    setAlertState2(false);
    const regex = /^.{4,10}$/;
    const regex_login = /^[^ @]{4,20}$/;

    if (regex.test(registerData.password) && regex_login.test(registerData.login)) {
        axios.post('http://localhost:5000/api/register', {username: registerData.login, password: registerData.password})
        .then(response => {
            if (response.data.access_token != null || response.data.access_token != '') {
                const token = response.data.access_token;
                const expiresAt = Date.now() + 24 * 60 * 60 * 1000;
                localStorage.setItem('token', token);
                localStorage.setItem('token_expiration', expiresAt);
                window.location.reload();
            }
        })
        .catch(error => {
            if (error.status == 409) {
                setAlertState3(true);
                return;
            }
            console.error('Ошибка запроса: ', error);
        })
    } else if (!regex.test(registerData.password)) {
        setAlertState1(true);
    } else if (!regex_login.test(registerData.login)) {
        setAlertState2(true);
    } else {
        handleRegisterClose();
    }
  }

  useEffect(() => {
    console.log(localStorage.getItem('token'));
    const expiration = localStorage.getItem('token_expiration');
    if (parseInt(expiration) - Date.now() <= 0 || expiration == null) {
        localStorage.removeItem('token_expiration');
        localStorage.removeItem('token');
    } else {
        setCheckToken(true);
    }
  });

 

  return (
    <div className='app-container'>
        <header className='Home-header'>
            <div>
                <h6 style={{marginLeft: 100, fontSize: 24, alignItems: 'center'}}><img style={{alignItems: 'center'}} src={logImg} />Транспонатор нот</h6>
            </div>
            <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
                {checkToken === false && <a style={{fontSize: 24, display: 'flex', justifyContent: 'center', alignItems: 'center', height: 35, background:'white', outlineColor:'white', cursor:'pointer'}} onClick={handleOpen}>Вход</a>}
                {checkToken === false && <Button style={{marginLeft: 20, marginRight: 100, fontSize: 24, height: 35, display: 'flex', justifyContent: 'center', alignItems: 'center', color:'#1B9A46', outlineColor: '#1B9A46', background: 'white', borderColor: '#1B9A46'}} onClick={handleOpen}>Регистрация</Button>}
                {checkToken === true && <Button style={{marginLeft: 20, marginRight: 100, fontSize: 24, height: 35, display: 'flex', justifyContent: 'center', alignItems: 'center', color:'#1B9A46', outlineColor: '#1B9A46', background: 'white', borderColor: '#1B9A46'}} onClick={handleExit}>Выход</Button>}
            </div>
        </header>
        <main className='Home-body'>
            <h4 style={{fontSize: 32}}>Онлайн транспонирование нот</h4>
            <p style={{fontSize: 20}}>Ноты из любого произведения для любого инструмента</p>
            
            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 50}}>
                <div className='Home-tile'>
                    {checkToken === true && <div><Button className='Home-tile-button' style={{color:'white', background: '#1B9A46', borderColor: '#1B9A46'}} onClick={handleLoadOpen}>Загрузить файл</Button> <input type="file" ref={fileInputRef} style={{display: 'none'}} onChange={handleFileChange}/></div>}
                    {checkToken === false && <Button className='Home-tile-button' style={{color:'white', background: '#1B9A46', borderColor: '#1B9A46'}} onClick={handleOpen}>Войти в аккаунт</Button>}
                    {checkToken === true && <p style={{color: '#C8C8C8'}}>Загрузите MIDI файл. Максимальный размер файла - 78 мб</p>}
                    {checkToken === false && <p style={{color: '#C8C8C8'}}>Для загрузки файла требуется войти или зарегистрироваться</p>}

                </div>
            </div>
            {loading === true && <img src={gif} style={{width: 50, height: 50}}/>}
            {loading === true && <p>Транспонирование...</p>}
            {fileUploadStatus === true && <a href={data.png} download="result" target="_blank" rel="noreferrer"><Button style={{color:'white', background: '#1B9A46', borderColor: '#1B9A46', width: 200, height: 70, fontSize: 25}}>Скачать PNG</Button></a>}
            {fileUploadStatus === true && <a href={data.pdf} download="result" target="_blank" rel="noreferrer"><Button style={{color:'white', background: '#1B9A46', borderColor: '#1B9A46', width: 200, height: 70, fontSize: 25, marginLeft: 20}}>Скачать PDF</Button></a>}
            {alertState4 === true && <p style={{color:'red'}}>Достигнут ежедневный лимит</p>}
        </main>
        <footer className='Home-footer'>
            <div style={{color: 'white', padding: '10px'}}>
                noteshift.net
            </div>
            <div style={{display: 'flex', justifyContent: 'center'}}>
                <a style={{color:'white', padding: '10px'}}>О нас</a>
                <a style={{color:'white', padding: '10px'}}>Безопасность</a>
                <a style={{color:'white', padding: '10px'}}>Стоимость</a>
                <a style={{color:'white', padding: '10px'}}>Помощь</a>
            </div>
            <div style={{color: 'white', padding: '10px'}}>
                Язык
            </div>
        </footer>
        <Modal show={modalState} onHide={handleClose} backdrop="static" keyboard={true}>
            <Modal.Header closeButton>
            <Modal.Title>Вход</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Form.Group className='mb-3'>
                        <Form.Label>Имя пользователя</Form.Label>
                        <Form.Control onChange={(e)=>{e.preventDefault(); loginData.login = e.target.value}} type='login'></Form.Control>
                    </Form.Group>
                    {alertState2 === true && <p style={{color:'red'}}>Логин должен быть длиной от 4 до 20 и не содержать в себе пробелы и символ @</p>}
                    <Form.Group className='mb-3'>
                        <Form.Label>Пароль</Form.Label>
                        <Form.Control onChange={(e)=>{e.preventDefault(); loginData.password = e.target.value}} type='password'></Form.Control>
                    </Form.Group>
                    {alertState1 === true && <p style={{color:'red'}}>Пароль должен быть длиной от 4 до 10</p>} 
                    {alertState3 === true && <p style={{color:'red'}}>Неправильный логин или пароль</p>}
                </Form>
            </Modal.Body>
            <Modal.Footer>
                
                <Button variant="secondary" onClick={handleClose}>
                    Закрыть окно
                </Button>
                <Button variant="primary" style={{color:'white', background: '#1B9A46', borderColor: '#1B9A46'}} onClick={handleLogin}>
                    Войти
                </Button>
            </Modal.Footer>
        </Modal>

        <Modal show={modalRegisterState} onHide={handleRegisterClose} backdrop="static" keyboard={true}>
            <Modal.Header closeButton>
            <Modal.Title>Регистрация</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Form.Group className='mb-3'>
                        <Form.Label>Имя пользователя</Form.Label>
                        <Form.Control onChange={(e)=>{e.preventDefault(); registerData.login = e.target.value}} type='login'></Form.Control>
                    </Form.Group>
                    {alertState2 === true && <p style={{color:'red'}}>Логин должен быть длиной от 4 до 20 и не содержать в себе пробелы и символ @</p>}
                    <Form.Group className='mb-3'>
                        <Form.Label>Пароль</Form.Label>
                        <Form.Control onChange={(e)=>{e.preventDefault(); registerData.password = e.target.value}}></Form.Control>
                    </Form.Group>
                    {alertState1 === true && <p style={{color:'red'}}>Пароль должен быть длиной от 4 до 10</p>} 
                </Form>
            </Modal.Body>
            <Modal.Footer>
                {alertState3 === true && <p style={{color:'red'}}>Пользователь уже существует</p>}
                <Button variant="secondary" onClick={handleRegisterClose}>
                    Закрыть окно
                </Button>
                <Button variant="primary" style={{color:'white', background: '#1B9A46', borderColor: '#1B9A46'}} onClick={handleRegister}>
                    Зарегистрироваться
                </Button>
            </Modal.Footer>
        </Modal>
    </div>
  );
}

export default Home;
