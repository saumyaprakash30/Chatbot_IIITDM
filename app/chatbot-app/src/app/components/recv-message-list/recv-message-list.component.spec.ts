import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecvMessageListComponent } from './recv-message-list.component';

describe('RecvMessageListComponent', () => {
  let component: RecvMessageListComponent;
  let fixture: ComponentFixture<RecvMessageListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RecvMessageListComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RecvMessageListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
