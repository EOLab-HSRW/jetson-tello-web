import { Component } from "react";
import styled from "styled-components";
import Hls from 'hls.js'

const PlayerWrapper = styled.div `
    position: relative
`
const PlayerInner = styled.div `
`

export default class Player extends Component{

    constructor(props){
        super(props);
        this._onTouchInsidePlayer= this._onTouchInsidePlayer.bind(this)
    }

    _onTouchInsidePlayer(){
        if (this.player.paused){
            this.player.play();
        } else {
            this.player.pause();
        }
    }
    
    componentDidMount(){

        const video = this.player;
        var streamUrl = 'http://192.168.30.17:3000/playlist.m3u8';//'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8';
        if (Hls.isSupported() && this.player) {
            const hls = new Hls();
            hls.loadSource(streamUrl);
            hls.attachMedia(video);

            hls.on(Hls.Events.MANIFEST_PARSED, function(){
                video.play();
            });
        }
    }

    render(){

        const style = {
            width: 640,
            height: 360,
            background: '#000'
        }

        return <PlayerWrapper>
            <PlayerInner>
            {/* controls={true} */}
                <video controls={true} onClick={this._onTouchInsidePlayer} style={style} ref={(player) => this.player = player}autoPlay={true}></video>
            </PlayerInner>
        </PlayerWrapper>
    }
}