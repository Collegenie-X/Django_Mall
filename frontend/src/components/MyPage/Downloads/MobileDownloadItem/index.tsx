// src/components/MyPage/Downloads/DownloadItem.tsx
import React from 'react';
import {
  Box,
  Typography,
  Button,
  Link as MuiLink,
  Divider,
} from '@mui/material';
import { styled } from '@mui/system';

import { Download } from '@/types/Downloads'; // 기존 Download 타입 임포트
import { formatDate } from '@/utiles/formatDate';
import CustomButton from '../../Components/CustomButton';
import { formatAmount } from '@/utiles/paymentList';

interface DownloadItemProps {
  download: Download;
  onReDownload: (fileUrl?: string) => void;
}

interface DownloadItemProps {
  download: Download;
  onReDownload: (fileUrl?: string) => void;
}

const StyledBox = styled(Box)({
  border: '1px solid #e4e4e4',
  backgroundColor: '#fff',
  borderRadius: '14px',
  padding: '16px',
  marginTop: 15,
  marginBottom: 15,
  boxShadow: 'rgba(100, 100, 111, 0.2) 0px 7px 12px 0px',
});

const DownloadItem: React.FC<DownloadItemProps> = ({
  download,
  onReDownload,
}) => {
  return (
    <StyledBox>
      <Typography
        variant="body2"
        gutterBottom
        sx={{ color: '#acacac', fontSize: 12, letterSpacing: -0.5, mb: 1 }}
      >
        {formatDate(download.downloaded_at)}
      </Typography>

      <Typography variant="body2" gutterBottom sx={{ color: '#9c9c9c' }}>
        <span style={{ color: '#acacac', width: 60, display: 'inline-block' }}>
          Subject
        </span>{' '}
        {download.problem_detail.subject}
      </Typography>
      <Typography variant="body2" gutterBottom sx={{ color: '#9c9c9c', mb: 2 }}>
        <span style={{ color: '#acacac', width: 60, display: 'inline-block' }}>
          Type
        </span>{' '}
        {download.problem_detail.type || 'No Type'}
      </Typography>

      <MuiLink
        href={`/store/${download.problem}`}
        underline="hover"
        sx={{
          cursor: 'pointer',
          lineHeight: 1.5,
          fontWeight: 'bold',
          color: '#5c5c5c',
          fontSize: 14,
        }}
      >
        {download.problem_detail.title}
      </MuiLink>
      <Box sx={{display:"flex" , alignItems:'center', gap:0.5 , fontSize:14 ,mt:0.5}}> 

      {Number(download.problem_detail.discounted_price) > 0 ? (
                        <Box>
                          {formatAmount(Number(download.problem_detail.discounted_price))}
                          <s style={{fontSize:"0.78em", color:"#acacac", marginLeft:2}}>{formatAmount(Number(download.problem_detail.price))}</s>{' '}
                        </Box>
                      ) : (
                        formatAmount(Number(download.problem_detail.price))
                      )}

                      {download.problem_detail.is_free &&  <span style={{fontSize:"0.78em", color:"#9c9c9c" }}> (free) </span>}

      </Box>

      <Box mt={2} textAlign={'right'}>
        <CustomButton
          label="Re-download"
          onClick={() => onReDownload(download.download_url)}
        />
      </Box>
    </StyledBox>
  );
};

export default DownloadItem;
