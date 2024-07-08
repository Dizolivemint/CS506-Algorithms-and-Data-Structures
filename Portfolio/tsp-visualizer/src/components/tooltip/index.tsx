import React, { useState } from 'react';
import styled from 'styled-components';

const TooltipContainer = styled.div`
  position: relative;
  display: inline-block;
  margin-left: 5px;
`;

const TooltipText = styled.div<{ visible: boolean }>`
  visibility: ${props => (props.visible ? 'visible' : 'hidden')};
  width: 200px;
  background-color: black;
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 5px;
  position: absolute;
  z-index: 1;
  bottom: 100%;
  left: 50%;
  margin-left: -100px;
  opacity: ${props => (props.visible ? 1 : 0)};
  transition: opacity 0.3s;
`;

const Tooltip: React.FC<{ text: string }> = ({ text }) => {
  const [visible, setVisible] = useState(false);

  return (
    <TooltipContainer>
      <span
        onMouseEnter={() => setVisible(true)}
        onMouseLeave={() => setVisible(false)}
        onClick={() => setVisible(!visible)}
        style={{ cursor: 'pointer', color: 'blue', textDecoration: 'underline' }}
      >
        ?
      </span>
      <TooltipText visible={visible}>{text}</TooltipText>
    </TooltipContainer>
  );
};

export default Tooltip;
