import React from "react";
import { bodyColor, borderColor, containerMaxWidth, headerHeight } from "./theme"
import styled from 'styled-components'
import Watch from "./watch";

const AppWrapper = styled.div `
`
const Container = styled.div`
    max-width : ${containerMaxWidth}px;
`

const Header = styled.h1`
    height: ${headerHeight}px;
    border-bottom: 1px solid ${borderColor};
`
const Main = styled.div`
    padding : 20px 0;
`
const Footer = styled.h1`
    border-top: 1px solid ${bodyColor};
    padding: 10px 0;
`
function App() {
    return (
        <AppWrapper>
            <Header>Header</Header>
            <Main>Main</Main>
            <Footer className="footer">
                <Container>
                    Main Component
                    <Watch></Watch>
                </Container>
            </Footer>
        </AppWrapper>
        )
}
export default App;