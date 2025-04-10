// src/components/MyPage/Downloads.tsx
'use client'; // Next.js 13 이상 사용 시 추가

import React, { useState } from 'react';
import {
  Box,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Divider,
  CircularProgress,
  Alert,
  useMediaQuery,
  Link,
} from '@mui/material';
import { styled, useTheme } from '@mui/system';
import CustomPagination from '@/components/Pagination'; // 커스텀 페이징 컴포넌트
import useDownloads from '@/hooks/useDownloadsAPI'; // 커스텀 훅
import DownloadItem from './MobileDownloadItem'; // 새로운 컴포넌트
import { formatDate } from '@/utiles/formatDate';
import { formatAmount } from '@/utiles/paymentList';

const HeaderCell = styled(TableCell)(({ theme }) => ({
  color: '#9a9a9a',
  fontWeight: 'bold',
  fontSize: 15,
  textAlign: 'center',
  border: 'none',
  padding: theme.spacing(1, 2),
}));

const BodyCell = styled(TableCell)(({ theme }) => ({
  textTransform: 'none',
  fontSize: 14,
  textAlign: 'center',
  border: 'none',
  padding: theme.spacing(1, 2),
}));

const itemsPerPage = 8;

const Downloads: React.FC = () => {
  const { downloads, downloadsMeta, isLoading, isError, error } =
    useDownloads();
  const [page, setPage] = useState(1);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm')); // 600px 이하

  const handleChangePage = (
    event: React.ChangeEvent<unknown>,
    value: number,
  ) => {
    setPage(value);
  };

  const handleReDownloadFile = (fileUrl?: string) => {
    if (fileUrl) {
      window.open(fileUrl, '_blank');
    } else {
      alert('파일 URL이 없습니다.');
    }
  };

  const displayedItems = downloads?.slice(
    (page - 1) * itemsPerPage,
    page * itemsPerPage,
  );

  if (isError) {
    return (
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '20vh',
        }}
      >
        <Alert severity="error">
          {error?.message || '다운로드 목록을 불러오는 중 오류가 발생했습니다.'}
          <Button onClick={() => window.location.reload()} sx={{ ml: 2 }}>
            다시 시도
          </Button>
        </Alert>
      </Box>
    );
  }

  return (
    <Box sx={{ mx: { sm: 0, md: 5 } }}>
      <Typography gutterBottom sx={{ fontSize: 28 }}>
        Downloads
      </Typography>
      <Divider
        sx={{
          borderBottomWidth: 4,
          background: '#ececec',
          mr: { sm: 2, md: 0 },
        }}
      />

      {isLoading ? (
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            minHeight: '25vh',
          }}
        >
          <CircularProgress />
        </Box>
      ) : (
        <>
          {isMobile ? (
            <Box sx={{}}>
              {displayedItems?.map((download) => (
                <DownloadItem
                  key={download.id}
                  download={download}
                  onReDownload={handleReDownloadFile}
                />
              ))}
            </Box>
          ) : (
            <TableContainer
              component="div"
              sx={{ border: 'none', boxShadow: 'none', my: 3, mx: 'auto' }}
            >
              <Table sx={{ maxWidth: '90vw' }}>
                <TableHead>
                  <TableRow sx={{ backgroundColor: 'var(--color-bg)' }}>
                    <HeaderCell>Problem Subject</HeaderCell>
                    <HeaderCell>Problem Type</HeaderCell>
                    <HeaderCell>Problem Title</HeaderCell>
                    <HeaderCell>Problem Price</HeaderCell>
                    <HeaderCell>Download Date</HeaderCell>
                    <HeaderCell
                      sx={{
                        letterSpacing: -0.5,
                        fontSize: 13,
                      }}
                    >
                      Re-download
                    </HeaderCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {displayedItems?.map((download) => (
                    <TableRow key={download.id}>
                      <BodyCell>{download.problem_detail.subject}</BodyCell>
                      <BodyCell sx={{ color: '#9c9c9c' }}>
                        {download.problem_detail.type || 'No Type'}
                      </BodyCell>
                      <BodyCell>
                        <Link
                          href={`/store/${download.problem_detail.id}`}
                          underline="hover"
                          color="inherit"
                          sx={{ cursor: 'pointer', fontSize: 14 }}
                        >
                          {download.problem_detail.title}
                        </Link>
                      </BodyCell>
                      <BodyCell>
                        {Number(download.problem_detail.discounted_price) >
                        0 ? (
                          <>
                            {formatAmount(
                              Number(download.problem_detail.discounted_price),
                            )}
                            <s
                              style={{
                                fontSize: '0.78em',
                                color: '#acacac',
                                marginLeft: 2,
                              }}
                            >
                              {formatAmount(
                                Number(download.problem_detail.price),
                              )}
                            </s>{' '}
                          </>
                        ) : (
                          formatAmount(Number(download.problem_detail.price))
                        )}

                        {download.problem_detail.is_free && (
                          <span
                            style={{ fontSize: '0.84em', color: '#9c9c9c' }}
                          >
                            {' '}
                            (free){' '}
                          </span>
                        )}
                      </BodyCell>

                      <BodyCell>
                        <Typography
                          sx={{
                            letterSpacing: -0.5,
                            wordSpacing: -0.5,
                            fontSize: 14,
                          }}
                        >
                          {formatDate(download.downloaded_at)}
                        </Typography>
                      </BodyCell>
                      <BodyCell>
                        <Button
                          variant="text"
                          sx={{
                            textDecoration: 'underline',
                            fontWeight: 'bold',
                            width: 80,
                            px: 0,
                            textTransform: 'none',
                            color: '#004B95',
                            letterSpacing: -0.5,
                            fontSize: 13,
                          }}
                          onClick={() =>
                            handleReDownloadFile(download.download_url)
                          }
                        >
                          Re-download
                        </Button>
                      </BodyCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </>
      )}

      <Divider sx={{ borderBottomWidth: 4, background: '#ececec' }} />

      <CustomPagination
        count={
          downloadsMeta && downloadsMeta.count !== undefined
            ? Math.ceil(downloadsMeta.count / itemsPerPage)
            : 0
        }
        page={page}
        onChange={handleChangePage}
      />
    </Box>
  );
};

export default Downloads;
